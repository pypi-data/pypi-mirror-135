# Generated by Django 3.1.8 on 2021-05-02 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AutomationModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "automation_class",
                    models.CharField(max_length=256, verbose_name="Process class"),
                ),
                (
                    "finished",
                    models.BooleanField(default=False, verbose_name="Finished"),
                ),
                ("data", models.JSONField(default=dict, verbose_name="Data")),
                (
                    "paused_until",
                    models.DateTimeField(null=True, verbose_name="Paused until"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="AutomationTaskModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(blank=True, max_length=256, verbose_name="Status"),
                ),
                ("locked", models.IntegerField(default=0, verbose_name="Locked")),
                (
                    "interaction_permissions",
                    models.JSONField(
                        default=list,
                        help_text="List of permissions of the form app_label.codename",
                        verbose_name="Required permissions",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("finished", models.DateTimeField(null=True)),
                (
                    "message",
                    models.CharField(
                        blank=True, max_length=128, verbose_name="Message"
                    ),
                ),
                (
                    "result",
                    models.JSONField(
                        blank=True, default=dict, null=True, verbose_name="Result"
                    ),
                ),
                (
                    "automation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="automations.automationmodel",
                    ),
                ),
                (
                    "interaction_group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="auth.group",
                        verbose_name="Assigned group",
                    ),
                ),
                (
                    "interaction_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Assigned user",
                    ),
                ),
                (
                    "previous",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="automations.automationtaskmodel",
                        verbose_name="Previous task",
                    ),
                ),
            ],
        ),
    ]
