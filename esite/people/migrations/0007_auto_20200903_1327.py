# Generated by Django 2.2 on 2020-09-03 11:27

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20200902_0017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personpage',
            name='link_collection',
        ),
        migrations.CreateModel(
            name='Meta_Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, max_length=255, null=True)),
                ('link_type', models.CharField(choices=[('INSTAGRAM_VIDEO', 'Instagram Post Video'), ('INSTAGRAM_PHOTO', 'Instagram Post Photo'), ('PHOTO', 'Photo URL'), ('YOUTUBE', 'Youtube URL'), ('other', 'Other')], default='other', max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('imgur_delete_hash', models.CharField(blank=True, max_length=255, null=True)),
                ('person_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta_links', to='people.PersonPage')),
            ],
        ),
    ]