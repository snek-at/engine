# Generated by Django 2.2.9 on 2020-01-30 21:33

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[],
            options={
                "ordering": ("date_joined",),
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("user.user",),
        ),
    ]
