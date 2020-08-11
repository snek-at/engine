from django.http import HttpResponse
from django.db import models
import django.contrib.auth.validators
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from wagtail.core.fields import RichTextField, StreamField, StreamBlock
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel,
    FieldPanel,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from esite.colorfield.fields import ColorField, ColorAlphaField
from esite.colorfield.blocks import ColorBlock, ColorAlphaBlock, GradientColorBlock

from esite.bifrost.helpers import register_streamfield_block

from esite.bifrost.models import (
    GraphQLForeignKey,
    GraphQLField,
    GraphQLStreamfield,
    GraphQLImage,
    GraphQLString,
    GraphQLCollection,
    GraphQLEmbed,
    GraphQLSnippet,
    GraphQLBoolean,
    GraphQLSnippet,
)

from esite.bifrost.models import (
    GraphQLField,
    GraphQLString,
    GraphQLStreamfield,
)

from esite.utils.models import BasePage

# Create your homepage related models here.


@register_streamfield_block
class _S_TopLanguages(blocks.StructBlock):
    theme = blocks.CharBlock(null=True,
                             blank=True,
                             help_text="Bold header text",
                             max_length=64)

    graphql_fields = [
        GraphQLString("theme"),
    ]


@register_streamfield_block
class _S_Calendar(blocks.StructBlock):
    theme = blocks.CharBlock(null=True,
                             blank=True,
                             help_text="Bold header text",
                             max_length=64)

    graphql_fields = [
        GraphQLString("theme"),
    ]


# > Profilepage
class Profile(models.Model):
    person = ParentalKey("people.PersonFormPage",
                         null=True,
                         related_name="profiles")
    platformName = models.CharField(null=True, blank=True, max_length=250)
    platformUrl = models.CharField(null=True, blank=True, max_length=250)
    avatarUrl = models.CharField(null=True, blank=True, max_length=250)
    websiteUrl = models.CharField(null=True, blank=True, max_length=250)
    company = models.CharField(null=True, blank=True, max_length=250)
    email = models.CharField(null=True, blank=True, max_length=250)
    username = models.CharField(null=True, blank=True, max_length=250)
    fullname = models.CharField(null=True, blank=True, max_length=250)
    createdAt = models.CharField(null=True, blank=True, max_length=250)
    location = models.CharField(null=True, blank=True, max_length=250)
    statusMessage = models.CharField(null=True, blank=True, max_length=250)
    statusEmojiHTML = models.CharField(null=True, blank=True, max_length=250)

    graphql_fields = [
        GraphQLString("platformName"),
        GraphQLString("platformUrl"),
        GraphQLString("avatarUrl"),
        GraphQLString("websiteUrl"),
        GraphQLString("company"),
        GraphQLString("email"),
        GraphQLString("username"),
        GraphQLString("fullname"),
        GraphQLString("createdAt"),
        GraphQLString("location"),
        GraphQLString("statusMessage"),
        GraphQLString("statusEmojiHTML"),
    ]

    # content_panels = [
    #     MultiFieldPanel(
    #         [
    #             FieldPanel("platformName"),
    #             FieldPanel("platformUrl"),
    #             FieldPanel("avatarUrl"),
    #             FieldPanel("websiteUrl"),
    #             FieldPanel("company"),
    #             FieldPanel("email"),
    #             FieldPanel("username"),
    #             FieldPanel("fullname"),
    #             FieldPanel("createdAt"),
    #             FieldPanel("location"),
    #             FieldPanel("statusMessage"),
    #             FieldPanel("statusEmojiHTML"),
    #             FieldPanel("bids"),
    #             FieldPanel("tids"),
    #         ],
    #     ),
    # ]

    # edit_handler = TabbedInterface(
    #     [
    #         ObjectList(
    #             content_panels, heading="Content"
    #         ),
    #     ]
    # )
