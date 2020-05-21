# Generated by Django 2.2.9 on 2020-01-30 21:33

from django.db import migrations, models
import django.db.models.deletion
import esite.home.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('city', models.CharField(max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('telephone', models.CharField(max_length=255, null=True)),
                ('telefax', models.CharField(max_length=255, null=True)),
                ('vat_number', models.CharField(max_length=255, null=True)),
                ('whatsapp_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('whatsapp_contactline', models.CharField(blank=True, max_length=255, null=True)),
                ('tax_id', models.CharField(max_length=255, null=True)),
                ('court_of_registry', models.CharField(max_length=255, null=True)),
                ('place_of_registry', models.CharField(max_length=255, null=True)),
                ('trade_register_number', models.CharField(max_length=255, null=True)),
                ('ownership', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('copyrightholder', models.CharField(max_length=255, null=True)),
                ('about', wagtail.core.fields.RichTextField(null=True)),
                ('privacy', wagtail.core.fields.RichTextField(null=True)),
                ('sociallinks', wagtail.core.fields.StreamField([('link', wagtail.core.blocks.URLBlock(help_text='Important! Format https://www.domain.tld/xyz'))])),
                ('headers', wagtail.core.fields.StreamField([('h_hero', wagtail.core.blocks.StructBlock([('slide_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Big, high resolution slider image', null=True)), ('slide_button', wagtail.snippets.blocks.SnippetChooserBlock(esite.home.models.Button, blank=True, help_text='The button displayed at the frontpage slider', null=True, required=False))], blank=False, icon='image', null=True)), ('code', wagtail.core.blocks.RawHTMLBlock(blank=True, classname='full', icon='code', null=True))], null=True)),
                ('sections', wagtail.core.fields.StreamField([('s_why', wagtail.core.blocks.StructBlock([('why_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('why_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('why_Columns', wagtail.core.blocks.StreamBlock([('why_Column', wagtail.core.blocks.StructBlock([('Column_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Icon representating the below content', null=True)), ('Column_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='The bold header text at the frontpage slider', null=True)), ('Column_subhead', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='The content of the frontpage slider element', null=True)), ('Column_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='Formatted text', null=True))], blank=False, icon='cogs', null=True))], blank=False, max_num=8, null=True))], blank=False, icon='group', null=True)), ('s_about', wagtail.core.blocks.StructBlock([('about_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('about_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('about_cards', wagtail.core.blocks.StreamBlock([('aboutcard', wagtail.core.blocks.StructBlock([('card_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Office-fitting image', null=True)), ('card_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='The bold header text at the frontpage slider', null=True)), ('card_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='Formatted text', null=True))], blank=False, icon='cogs', null=True))], blank=False, max_num=6, null=True))], blank=False, icon='fa-quote-left', null=True)), ('s_instagram', wagtail.core.blocks.StructBlock([('instagram_id', wagtail.core.blocks.CharBlock(blank=False, classname='full', help_text='Instagram-Account id', null=True)), ('instagram_pc', wagtail.core.blocks.CharBlock(blank=False, classname='full', help_text='Instagram-Post count', null=True))], blank=False, icon='fa-instagram', null=True)), ('s_steps', wagtail.core.blocks.StructBlock([('steps_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('steps_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('steps_steps', wagtail.core.blocks.StreamBlock([('step', wagtail.core.blocks.StructBlock([('step_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Image fitting this step', null=True)), ('step_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('step_subhead', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='Short introduction to the following paragraph', null=True)), ('step_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='Step paragraph', null=True))], blank=False, null=True))], blank=False, max_num=4, null=True))], blank=False, icon='fa-list-ul', null=True)), ('s_shop', wagtail.core.blocks.StructBlock([('shop_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('shop_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False))], blank=False, icon='home', null=True)), ('s_trusted', wagtail.core.blocks.StructBlock([('trusted_partner', wagtail.core.blocks.StreamBlock([('partner', wagtail.core.blocks.StructBlock([('partner_logo', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Image fitting this step', null=True)), ('partner_link', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True))], blank=False, null=True))], blank=False, max_num=4, null=True))], blank=False, icon='fa-list-ul', null=True)), ('s_wolf', wagtail.core.blocks.StructBlock([('wolf_head', wagtail.core.blocks.CharBlock(blank=False, classname='full', help_text='Bold header text', null=True)), ('wolf_subhead', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='The content of the black wolf coffee intro', null=True))], blank=False, icon='fa-list-ul', null=True)), ('s_faq', wagtail.core.blocks.StructBlock([('header', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('questions', wagtail.core.blocks.StreamBlock([('question', wagtail.core.blocks.StructBlock([('question_icon', wagtail.core.blocks.CharBlock(blank=True, help_text='Font Awesome icon name (e.g. facebook-f) from https://fontawesome.com/icons?d=gallery&s=solid&m=free', null=True)), ('question_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('question_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', help_text='Formatted text', null=True)), ('question_link', wagtail.core.blocks.URLBlock(blank=True, help_text='Important! Format https://www.domain.tld/xyz', null=True))], blank=False, null=True))], blank=False, max_num=4, null=True))], blank=False, icon='home', null=True)), ('code', wagtail.core.blocks.RawHTMLBlock(blank=True, classname='full', icon='code', null=True))], null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_title', models.CharField(max_length=255, null=True)),
                ('button_embed', models.CharField(blank=True, max_length=255, null=True)),
                ('button_link', models.URLField(blank=True, null=True)),
                ('button_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
            ],
        ),
    ]
