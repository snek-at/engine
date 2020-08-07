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
)

from esite.utils.models import BasePage

# Create your homepage related models here.

@register_streamfield_block
class _E_CommentBlock(blocks.StructBlock):
    comment_owner = blocks.PageChooserBlock(null=True, required=False, target_model="profile.ProfilePage", help_text="Owner of the comment")
    comment_datetime = blocks.DateTimeBlock(null=True, required=False)
    comment_message = blocks.TextBlock(null=True, required=False,  help_text="Other information")

    graphql_fields = [GraphQLString("comment_owner"), GraphQLString("comment_datetime"), GraphQLString("comment_message"),]


class Talk(models.Model):
    talk_id = models.CharField(primary_key=True, max_length=36)
    talk_title = models.CharField(null=True, blank=True, max_length=32)
    talk_description= blocks.TextBlock(null=True, required=False,  help_text="Other information")
    talk_path = models.CharField(null=True, blank=True, max_length=256)
    talk_url = models.URLField(null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz")
    talk_displayUrl = models.URLField(null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz")
    talk_downloadUrl = models.URLField(null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz")
    talk_comments = StreamField([
        ('e_comment', _E_CommentBlock(null=True, icon='fa-id-badge')),
    ], null=True, blank=False)


    graphql_fields = [
        GraphQLString("talk_id"),
        GraphQLString("talk_title"),
        GraphQLString("talk_description"),
        GraphQLString("talk_path"),
        GraphQLString("talk_url"),
        GraphQLString("talk_displayUrl"),
        GraphQLString("talk_downloadUrl"),
        GraphQLStreamfield("talk_comments"),
    ]

    main_content_panels = [
        FieldPanel("talk_id"),
        FieldPanel("talk_title"),
        FieldPanel("talk_description"),
        FieldPanel("talk_path"),
        FieldPanel("talk_url"),
        FieldPanel("talk_displayUrl"),
        FieldPanel("talk_downloadUrl"),
        StreamFieldPanel("talk_comments")
    ]


    edit_handler = TabbedInterface(
        [
            ObjectList(main_content_panels, heading="Content"),
        ]
    )
