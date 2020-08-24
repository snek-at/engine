import django.contrib.auth.validators
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    FieldPanel,
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


@register_streamfield_block
class Meta_Link(blocks.StructBlock):
    LINK_TYPES = (
        ("instagram_video", "Instagram Post Video"),
        ("instagram_photo", "Instagram Post Photo"),
        ("other", "Other"),
    )

    url = blocks.URLBlock(null=True, blank=True, max_length=255)
    link_type = blocks.ChoiceBlock(choices=LINK_TYPES, default="other")

    # > Meta
    location = blocks.CharBlock(null=True, blank=True, max_length=255)
    description = blocks.TextBlock(null=True, blank=True)


# > Profilepage
class Profile(models.Model):
    person_page = ParentalKey(
        "people.PersonFormPage", null=True, related_name="profiles"
    )
    platform_name = models.CharField(null=True, blank=True, max_length=250)

    link_collection = StreamField([("link", Meta_Link())], null=True, blank=True)

    graphql_fields = [
        GraphQLString("id"),
        GraphQLString("platform_name"),
        GraphQLStreamfield("link_collection"),
    ]

    content_panels = [
        FieldPanel("person_page"),
        MultiFieldPanel(
            [FieldPanel("platform_name"), StreamFieldPanel("link_collection"),],
        ),
    ]

    # data_panels = [MultiFieldPanel([StreamFieldPanel("link_collection"),])]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            # ObjectList(data_panels, heading="Data"),
        ]
    )
