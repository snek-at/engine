import django.contrib.auth.validators
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    RichTextFieldPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamBlock, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from esite.bifrost.helpers import register_streamfield_block
from esite.bifrost.models import (
    GraphQLBoolean,
    GraphQLCollection,
    GraphQLEmbed,
    GraphQLField,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLSnippet,
    GraphQLStreamfield,
    GraphQLString,
)
from esite.colorfield.blocks import ColorAlphaBlock, ColorBlock, GradientColorBlock
from esite.colorfield.fields import ColorAlphaField, ColorField
from esite.utils.models import BasePage

# Create your homepage related models here.


@register_streamfield_block
class _S_TopLanguages(blocks.StructBlock):
    theme = blocks.CharBlock(
        null=True, blank=True, help_text="Bold header text", max_length=64
    )

    graphql_fields = [
        GraphQLString("theme"),
    ]


@register_streamfield_block
class _S_Calendar(blocks.StructBlock):
    theme = blocks.CharBlock(
        null=True, blank=True, help_text="Bold header text", max_length=64
    )

    graphql_fields = [
        GraphQLString("theme"),
    ]


# > Profilepage
class Profile(models.Model):
    person_page = ParentalKey(
        "people.PersonFormPage", null=True, related_name="profiles"
    )
    name = models.CharField(null=True, blank=True, max_length=255)
    src_url = models.URLField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    company = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(null=True, blank=True, max_length=255)
    fullname = models.CharField(null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=255)
    status_message = models.CharField(null=True, blank=True, max_length=255)
    status_emoji_html = models.CharField(null=True, blank=True, max_length=255)

    graphql_fields = [
        GraphQLString("id"),
        GraphQLString("name"),
        GraphQLString("src_url"),
        GraphQLString("avatar_url"),
        GraphQLString("website_url"),
        GraphQLString("company"),
        GraphQLString("email"),
        GraphQLString("username"),
        GraphQLString("fullname"),
        GraphQLString("created_at"),
        GraphQLString("location"),
        GraphQLString("status_message"),
        GraphQLString("status_emoji_html"),
    ]

    content_panels = [
        FieldPanel("person_page"),
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("src_url"),
                FieldPanel("avatar_url"),
                FieldPanel("website_url"),
                FieldPanel("company"),
                FieldPanel("email"),
                FieldPanel("username"),
                FieldPanel("fullname"),
                FieldPanel("created_at"),
                FieldPanel("location"),
                FieldPanel("status_message"),
                RichTextFieldPanel("status_emoji_html"),
            ],
        ),
    ]

    # data_panels = [MultiFieldPanel([StreamFieldPanel("link_collection"),])]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            # ObjectList(data_panels, heading="Data"),
        ]
    )
