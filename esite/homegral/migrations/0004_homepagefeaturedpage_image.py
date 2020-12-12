# Generated by Django 2.1.7 on 2019-03-24 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20190322_2207'),
        ('home', '0003_auto_20190324_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagefeaturedpage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
    ]