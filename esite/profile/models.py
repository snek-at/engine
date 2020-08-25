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
from esite.utils.models import BasePage, TimeStampMixin


# Create your homepage related models here.
# > Profilepage
class Profile(TimeStampMixin):
    PROFILE_TYPES = (
        ("github", "GitHub"),
        ("gitlab", "GitLab"),
        ("instagram", "Instagram"),
    )
    person_page = ParentalKey(
        "people.PersonFormPage", null=True, related_name="profiles"
    )
    username = models.CharField(null=True, blank=True, max_length=255)
    token = models.CharField(null=True, blank=True, max_length=255)
    type = models.CharField(
        null=True, blank=False, choices=PROFILE_TYPES, max_length=255
    )

    graphql_fields = [
        GraphQLString("id"),
        GraphQLString("username"),
        GraphQLString("token"),
        GraphQLString("type"),
        GraphQLString("created_at"),
        GraphQLString("updated_at"),
    ]

    content_panels = [
        FieldPanel("person_page"),
        MultiFieldPanel(
            [FieldPanel("username"), FieldPanel("token"), FieldPanel("type"),],
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            # ObjectList(data_panels, heading="Data"),
        ]
    )
