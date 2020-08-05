# Generated by Django 2.2.12 on 2020-08-05 08:08

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="headers",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "code",
                        wagtail.core.blocks.RawHTMLBlock(
                            blank=True, classname="full", icon="code", null=True
                        ),
                    )
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="sections",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "code",
                        wagtail.core.blocks.RawHTMLBlock(
                            blank=True, classname="full", icon="code", null=True
                        ),
                    )
                ],
                null=True,
            ),
        ),
    ]
