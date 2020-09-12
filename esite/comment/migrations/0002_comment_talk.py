# Generated by Django 2.2 on 2020-09-02 11:58

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comment', '0001_initial'),
        ('talk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='talk',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_comments', to='talk.Talk'),
        ),
    ]