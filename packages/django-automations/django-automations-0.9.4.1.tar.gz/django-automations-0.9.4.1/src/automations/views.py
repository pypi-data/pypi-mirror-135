# coding=utf-8

# Create your views here.
import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms import BaseForm
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from . import flow, models, settings


class AutomationMixin:
    _automation_instance = None  # Buffer class for specific task_instance
    _task_id = None

    def get_automation_instance(self, task):
        if self._automation_instance is None or self._task_id != task.id:
            self._automation_instance = task.automation.instance
            self._task_id = task.id
        return self._automation_instance


class TaskView(LoginRequiredMixin, AutomationMixin, FormView):
    def bind_to_node(self):
        self.task = get_object_or_404(
            models.AutomationTaskModel, id=self.kwargs["task_id"]
        )
        self.node = self.task.get_node()

    def get_form_kwargs(self):
        assert hasattr(self, "node"), "Not bound to node"
        kwargs = super().get_form_kwargs()
        task_kwargs = self.node._form_kwargs
        kwargs.update(task_kwargs(self.task) if callable(task_kwargs) else task_kwargs)
        return kwargs

    def get_form_class(self):
        if not hasattr(self, "node"):
            self.bind_to_node()
        form = self.node._form
        return form if issubclass(form, BaseForm) else form(self.task)

    def get_context_data(self, **kwargs):
        if not hasattr(self, "node"):
            self.bind_to_node()
        if not isinstance(self.node, flow.Form):
            raise Http404
        if self.request.user not in self.task.get_users_with_permission():
            raise PermissionDenied
        if self.task.finished:
            raise Http404  # Need to display a message: s.o. else has completed form
        self.template_name = self.node._template_name or getattr(
            self.get_automation_instance(self.task),
            "default_template_name",
            "automations/form_view.html",
        )
        context = super().get_context_data(**kwargs)
        context.update(settings.FORM_VIEW_CONTEXT)
        context.update(getattr(self.node._automation, "context", dict()))
        context.update(self.node._context)
        return context

    def form_valid(self, form):
        self.node.is_valid(self.task, self.request, form)
        if self.node._run:
            self.node._automation.run(self.task.previous, self.node)
        if getattr(self.node, "_success_url", None):
            return redirect(self.node._success_url)
        elif "back" in self.request.GET:
            return redirect(self.request.GET.get("back"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("automations:task_list")


class TaskListView(LoginRequiredMixin, TemplateView):
    template_name = "automations/task_list.html"

    def get_context_data(self, **kwargs):
        qs = models.AutomationTaskModel.get_open_tasks(self.request.user)
        return dict(error="", tasks=qs, count=len(qs))


class UserIsStaff(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class TaskDashboardView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        "automations.view_automationmodel",
        "automations.view_automationtaskmodel",
    )
    template_name = "automations/dashboard.html"

    def get_context_data(self, **kwargs):
        days = self.request.GET.get("history", "")
        days = int(days) if days.isnumeric() else 30
        if days > 0:
            qs = models.AutomationModel.objects.filter(
                Q(created__gte=now() - datetime.timedelta(days=days))
                | Q(finished=False)  # Not older than days  # or still runnning
            ).order_by("-created")
        else:
            qs = models.AutomationModel.objects.order_by("-created")
        automations = []
        for item in (
            qs.order_by("automation_class").values("automation_class").distinct()
        ):
            qs_filtered = qs.filter(**item)
            try:
                automation = models.get_automation_class(item["automation_class"])
                verbose_name = automation.get_verbose_name()
                verbose_name_plural = automation.get_verbose_name_plural()
                dashboard_template = getattr(
                    getattr(automation, "Meta", None), "dashboard_template", ""
                )
                dashboard = (
                    automation.get_dashboard_context(qs_filtered)
                    if hasattr(automation, "get_dashboard_context")
                    else dict()
                )
            except AttributeError:
                verbose_name = (
                    _("Obsolete automation %s")
                    % item["automation_class"].rsplit(".")[-1]
                )
                verbose_name_plural = (
                    _("Obsolete automations %s")
                    % item["automation_class"].rsplit(".")[-1]
                )
                dashboard_template = ""
                dashboard = dict()
            if dashboard_template is not None:
                automations.append(
                    dict(
                        cls=item["automation_class"],
                        verbose_name=verbose_name,
                        verbose_name_plural=verbose_name_plural,
                        running=qs_filtered.filter(finished=False),
                        finished=qs_filtered.filter(finished=True),
                        dashboard_template=dashboard_template,
                        dashboard=dashboard,
                    )
                )
        return dict(automations=automations, timespan=_("Last %d days") % days)


class AutomationHistoryView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        "automations.change_automationmodel",
        "automations.change_automationtaskmodel",
    )
    template_name = "automations/history.html"

    def build_tree(self, task):
        result = []
        tasks = [task]
        while tasks:
            if len(tasks) > 1:  # Split
                lst = []
                for tsk in tasks:
                    sub_tree, next_task = self.build_tree(tsk)
                    lst.append(sub_tree)
                result.append(lst)
                if next_task:
                    result.append(next_task)
                tasks = next_task.get_next_tasks() if next_task else []
            else:
                task = tasks[0]
                if task.message == "Joined":  # Closed Join
                    return result, task
                result.append(task)
                tasks = task.get_next_tasks()
        return result, None

    def get_context_data(self, **kwargs):
        assert "automation_id" in kwargs
        automation = get_object_or_404(
            models.AutomationModel, id=kwargs.get("automation_id")
        )
        task = automation.automationtaskmodel_set.get(previous=None)
        tasks, _ = self.build_tree(task)
        return dict(
            automation=automation,
            tasks=tasks,
        )


class AutomationTracebackView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        "automations.change_automationmodel",
        "automations.change_automationtaskmodel",
    )
    template_name = "automations/traceback.html"

    def get_context_data(self, **kwargs):
        assert "automation_id" in kwargs
        assert "task_id" in kwargs
        automation = get_object_or_404(
            models.AutomationModel, id=kwargs.get("automation_id")
        )
        task = get_object_or_404(models.AutomationTaskModel, id=kwargs.get("task_id"))
        if task.automation != automation:
            raise Http404()
        if isinstance(task.result, dict):
            return dict(
                automation=automation,
                error=task.result.get("error", None),
                html=task.result.get("html", None),
            )
        return dict()


class AutomationErrorsView(PermissionRequiredMixin, TemplateView):
    permission_required = (
        "automations.change_automationmodel",
        "automations.change_automationtaskmodel",
    )
    template_name = "automations/error_report.html"

    def get_context_data(self, **kwargs):
        tasks = models.AutomationTaskModel.objects.filter(message__contains="Error")
        automations = []
        done = []
        for task in tasks:
            if task.automation.id not in done:
                done.append(task.automation.id)
                automations.append(
                    (task.automation, tasks.filter(automation=task.automation))
                )
        return dict(automations=automations)
