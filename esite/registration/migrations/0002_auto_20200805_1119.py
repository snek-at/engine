# Generated by Django 2.2.12 on 2020-08-05 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="registrationformsubmission",
            options={
                "verbose_name": "form submission",
                "verbose_name_plural": "form submissions",
            },
        ),
    ]