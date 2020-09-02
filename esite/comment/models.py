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
from esite.utils.models import TimeStampMixin

# Create your homepage related models here.


class Comment(TimeStampMixin, ClusterableModel):
    talk = ParentalKey(
        "talk.Talk", on_delete=models.CASCADE, related_name="talk_comments"
    )
    author = ParentalKey(
        "people.PersonPage", on_delete=models.CASCADE, related_name="author_comments",
    )
    text = models.TextField(null=True, blank=True, help_text="Comment text")
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    main_content_panels = [
        FieldPanel("author"),
        FieldPanel("text"),
        MultiFieldPanel([FieldPanel("talk")], heading="Associated instances"),
        MultiFieldPanel(
            [FieldPanel("created_at"), FieldPanel("updated_at")], heading="Meta",
        ),
        InlinePanel("reply_to"),
    ]

    graphql_fields = [
        GraphQLString("author"),
        GraphQLString("text"),
        GraphQLString("created_at"),
        GraphQLString("updated_at"),
        GraphQLForeignKey("replies", "comment.Comment", is_list=True),
    ]
