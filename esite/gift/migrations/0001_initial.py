# Generated by Django 2.2.9 on 2020-01-30 21:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GiftCode",
            fields=[
                (
                    "hkey",
                    models.CharField(max_length=14, primary_key=True, serialize=False),
                ),
                (
                    "bid",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="nomatch",
                                message="It has to be a md5 hash",
                                regex="^[a-f0-9]{32}$",
                            )
                        ],
                    ),
                ),
                (
                    "tid",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="nomatch",
                                message="It has to be a md5 hash",
                                regex="^[a-f0-9]{32}$",
                            )
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
