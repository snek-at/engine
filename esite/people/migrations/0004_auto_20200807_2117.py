# Generated by Django 2.2.12 on 2020-08-07 19:17

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailcore', '0047_auto_20200807_1358'),
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('registration', '0001_initial'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('images', '0002_auto_20200729_2232'),
        ('people', '0003_auto_20190324_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('social_text', models.CharField(blank=True, max_length=255)),
                ('listing_title', models.CharField(blank=True, help_text='Override the page title used when this page appears in listings', max_length=255)),
                ('listing_summary', models.CharField(blank=True, help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.", max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('display_email', models.BooleanField(blank=True, default=False)),
                ('workplace', models.CharField(blank=True, max_length=255)),
                ('display_workplace', models.BooleanField(blank=True, default=False)),
                ('job_title', models.CharField(blank=True, max_length=255)),
                ('website', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('rank', models.CharField(blank=True, max_length=1)),
                ('display_rank', models.BooleanField(blank=True, default=False)),
                ('display_languages', models.BooleanField(blank=True, default=False)),
                ('status', models.TextField(blank=True)),
                ('bio', models.TextField(blank=True)),
                ('listing_image', models.ForeignKey(blank=True, help_text='Choose the image you wish to be displayed when this page appears in listings', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage')),
                ('social_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.SNEKImage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.AlterField(
            model_name='socialmediaprofile',
            name='person_page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_profile', to='people.PersonFormPage'),
        ),
        migrations.DeleteModel(
            name='PersonPage',
        ),
    ]
