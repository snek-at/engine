import uuid

from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
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
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from esite.bifrost.helpers import register_streamfield_block
from esite.bifrost.models import (
    GraphQLCollection,
    GraphQLField,
    GraphQLForeignKey,
    GraphQLPage,
    GraphQLStreamfield,
    GraphQLString,
)
from esite.colorfield.blocks import ColorAlphaBlock, ColorBlock, GradientColorBlock
from esite.colorfield.fields import ColorAlphaField, ColorField
from esite.utils.models import BasePage

# Create your homepage related models here.


class Comment(models.Model):
    talk = ParentalKey(
        "talk.Talk", on_delete=models.CASCADE, related_name="comment_talk"
    )
    owner = ParentalKey(
        "people.PersonFormPage", on_delete=models.CASCADE, related_name="comment_owner"
    )
    datetime = models.DateTimeField(null=True, blank=True)
    message = models.TextField(null=True, blank=True, help_text="Other information")

    main_content_panels = [
        FieldPanel("talk"),
        FieldPanel("owner"),
        FieldPanel("datetime"),
        FieldPanel("message"),
    ]

    graphql_fields = [
        GraphQLString("talk"),
        GraphQLString("owner"),
        GraphQLString("datetime"),
        GraphQLString("message"),
    ]
