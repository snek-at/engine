# Generated by Django 2.2.9 on 2020-01-30 21:33

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfilePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                ("sources", models.TextField(null=True)),
                ("platform_data", models.TextField(blank=True, null=True)),
                ("verified", models.BooleanField(blank=True, default=False)),
                ("available_for_hire", models.BooleanField(blank=True, default=False)),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 36 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=36,
                        null=True,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=30, null=True)),
                ("last_name", models.CharField(blank=True, max_length=150, null=True)),
                ("telephone", models.CharField(blank=True, max_length=40, null=True)),
                ("address", models.CharField(blank=True, max_length=60, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=12, null=True)),
                ("city", models.CharField(blank=True, max_length=60, null=True)),
                ("country", models.CharField(blank=True, max_length=2, null=True)),
                ("newsletter", models.BooleanField(blank=True, default=False)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("website", models.URLField(blank=True, null=True)),
                ("company", models.CharField(blank=True, max_length=80, null=True)),
                ("bids", models.TextField(blank=True, null=True)),
                ("tids", models.TextField(blank=True, null=True)),
                (
                    "main",
                    wagtail.core.fields.StreamField(
                        [
                            (
                                "top_language",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "theme",
                                            wagtail.core.blocks.CharBlock(
                                                blank=True,
                                                help_text="Bold header text",
                                                max_length=64,
                                                null=True,
                                            ),
                                        )
                                    ],
                                    blank=True,
                                    icon="fa-instagram",
                                    null=True,
                                ),
                            ),
                            (
                                "calendar",
                                wagtail.core.blocks.StructBlock(
                                    [
                                        (
                                            "theme",
                                            wagtail.core.blocks.CharBlock(
                                                blank=True,
                                                help_text="Bold header text",
                                                max_length=64,
                                                null=True,
                                            ),
                                        )
                                    ],
                                    blank=True,
                                    icon="home",
                                    null=True,
                                ),
                            ),
                        ],
                        blank=True,
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("wagtailcore.page",),
        ),
    ]
