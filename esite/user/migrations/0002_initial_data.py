# -*- coding: utf-8 -*-
from django.db import migrations
from django.contrib.auth import get_user_model


def create_initialuser(apps, schema_editor):
    # Get models
    User = get_user_model()

    # Create anonymous user
    anonuser = User.objects.create(username="cisco", is_customer=False,)

    anonuser.set_password("ciscocisco")

    anonuser.save()

    # Create admin user
    adminuser = User.objects.create(username="admin", is_superuser=True,)

    adminuser.set_password("ciscocisco")

    adminuser.save()


def remove_initialuser(apps, schema_editor):
    # Get models
    User = get_user_model()

    # Delete the anonymous user
    User.objects.get(username="cisco").delete()

    # Delete the admin user
    User.objects.get(username="admin").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initialuser, remove_initialuser),
    ]
