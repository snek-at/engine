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


class Talk(ClusterableModel):
    #talk_id = models.CharField(primary_key=True, max_length=36)
    owner = ParentalKey("user.SNEKUser",
                        on_delete=models.CASCADE,
                        related_name="talk_owner")
    title = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(null=True,
                                   blank=True,
                                   help_text="Other information")
    path = models.CharField(null=True, blank=True, max_length=256)
    url = models.URLField(
        null=True,
        blank=True,
        help_text="Important! Format https://www.domain.tld/xyz")
    displayUrl = models.URLField(
        null=True,
        blank=True,
        help_text="Important! Format https://www.domain.tld/xyz")
    downloadUrl = models.URLField(
        null=True,
        blank=True,
        help_text="Important! Format https://www.domain.tld/xyz")

    graphql_fields = [
        #GraphQLString("talk_id"),
        GraphQLString("title"),
        GraphQLString("description"),
        GraphQLString("path"),
        GraphQLString("url"),
        GraphQLString("displayUrl"),
        GraphQLString("downloadUrl"),
        GraphQLCollection(GraphQLForeignKey, "comment_talk",
                          "comment.Comment"),
    ]

    main_content_panels = [
        FieldPanel("owner"),
        FieldPanel("title"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("path"),
        FieldPanel("url"),
        FieldPanel("displayUrl"),
        FieldPanel("downloadUrl"),
        InlinePanel('comment_talk', label='Comments'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading="Content"),
    ])
