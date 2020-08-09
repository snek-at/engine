# Generated by Django 2.1.7 on 2019-03-23 23:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        migrations.swappable_dependency(settings.WAGTAILIMAGES_IMAGE_MODEL),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PersonIndexPage',
            new_name='PersonIndex',
        ),
    ]
