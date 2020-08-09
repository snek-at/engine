# Generated by Django 2.1.7 on 2019-03-22 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        migrations.swappable_dependency(settings.WAGTAILIMAGES_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('social_text', models.CharField(blank=True, max_length=255)),
                ('listing_title', models.CharField(blank=True, help_text='Override the page title used when this page appears in listings', max_length=255)),
                ('listing_summary', models.CharField(blank=True, help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.", max_length=255)),
                ('introduction', models.TextField(blank=True)),
                ('listing_image', models.ForeignKey(blank=True, help_text='Choose the image you wish to be displayed when this page appears in listings', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.WAGTAILIMAGES_IMAGE_MODEL)),
                ('social_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.WAGTAILIMAGES_IMAGE_MODEL)),
            ],
            options={
                'verbose_name': 'Person Index',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='PersonPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('social_text', models.CharField(blank=True, max_length=255)),
                ('listing_title', models.CharField(blank=True, help_text='Override the page title used when this page appears in listings', max_length=255)),
                ('listing_summary', models.CharField(blank=True, help_text="The text summary used when this page appears in listings. It's also used as the description for search engines if the 'Search description' field above is not defined.", max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('introduction', models.TextField(blank=True)),
                ('biography', wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='title', template='patterns/molecules/streamfield/blocks/heading_block.html')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('quote', wagtail.core.blocks.StructBlock([('quote', wagtail.core.blocks.CharBlock(classname='title')), ('attribution', wagtail.core.blocks.CharBlock(required=False)), ('citation_link', wagtail.core.blocks.URLBlock(required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock()), ('document', wagtail.core.blocks.StructBlock([('document', wagtail.documents.blocks.DocumentChooserBlock()), ('title', wagtail.core.blocks.CharBlock(required=False))]))], blank=True)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('listing_image', models.ForeignKey(blank=True, help_text='Choose the image you wish to be displayed when this page appears in listings', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.WAGTAILIMAGES_IMAGE_MODEL)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.WAGTAILIMAGES_IMAGE_MODEL)),
                ('social_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.WAGTAILIMAGES_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='SocialMediaProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('twitter', 'Twitter'), ('linkedin', 'LinkedIn')], max_length=200)),
                ('username', models.CharField(max_length=255)),
                ('person_page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_profile', to='person.PersonPage')),
            ],
        ),
    ]
