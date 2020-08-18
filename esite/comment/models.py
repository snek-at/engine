import uuid
from django.http import HttpResponse
from django.db import models
from wagtail.core.fields import RichTextField, StreamField
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
from modelcluster.fields import ParentalKey

from esite.colorfield.fields import ColorField, ColorAlphaField
from esite.colorfield.blocks import ColorBlock, ColorAlphaBlock, GradientColorBlock
from esite.bifrost.helpers import register_streamfield_block
from esite.bifrost.models import (
    GraphQLField,
    GraphQLString,
    GraphQLStreamfield,
    GraphQLPage,
    GraphQLCollection,
    GraphQLForeignKey,
)

from esite.utils.models import BasePage

from modelcluster.models import ClusterableModel

# Create your homepage related models here.


class Comment(models.Model):
    talk = ParentalKey(
        "talk.Talk", on_delete=models.CASCADE, related_name="comment_talk"
    )
    owner = ParentalKey(
        "user.SNEKUser", on_delete=models.CASCADE, related_name="comment_owner"
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
