import uuid
from django.http import HttpResponse
from django.db import models
from django.conf import settings
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
from modelcluster.fields import ParentalKey, ParentalManyToManyField

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
    GraphQLImage,
    GraphQLInt,
)

from esite.utils.models import BasePage

from modelcluster.models import ClusterableModel

# Create your homepage related models here.


class Achievement(ClusterableModel):
    collectors = ParentalManyToManyField(
        "people.PersonFormPage", related_name="achievements", blank=True
    )
    title = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(null=True, blank=True, help_text="Other information")
    image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    points = models.IntegerField(default=0)

    graphql_fields = [
        GraphQLCollection(GraphQLForeignKey, "collectors", "achievement.Achievement"),
        GraphQLString("title"),
        GraphQLImage("image"),
        GraphQLInt("points"),
    ]

    main_content_panels = [
        FieldPanel("collectors"),
        FieldPanel("title"),
        FieldPanel("description"),
        ImageChooserPanel("image"),
        FieldPanel("points"),
    ]

    edit_handler = TabbedInterface(
        [ObjectList(main_content_panels, heading="Content"),]
    )

    def __str__(self):
        return f"{self.title} ({self.points})"
