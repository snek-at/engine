# Generated by Django 2.2 on 2020-08-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="enterpriseregistrationformfield",
            name="clean_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Safe name of the form field, the label converted to ascii_snake_case",
                max_length=255,
                verbose_name="name",
            ),
        ),
        migrations.AddField(
            model_name="personregistrationformfield",
            name="clean_name",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Safe name of the form field, the label converted to ascii_snake_case",
                max_length=255,
                verbose_name="name",
            ),
        ),
    ]
