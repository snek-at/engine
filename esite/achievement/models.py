import uuid

from django.conf import settings
from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey, ParentalManyToManyField
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
    GraphQLImage,
    GraphQLInt,
    GraphQLPage,
    GraphQLStreamfield,
    GraphQLString,
)
from esite.colorfield.blocks import ColorAlphaBlock, ColorBlock, GradientColorBlock
from esite.colorfield.fields import ColorAlphaField, ColorField
from esite.utils.edit_handlers import ReadOnlyPanel
from esite.utils.models import BasePage, TimeStampMixin

# Create your homepage related models here.


class Achievement(TimeStampMixin, ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collectors = ParentalManyToManyField(
        "people.PersonPage", related_name="achievements", blank=True
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
        GraphQLString("description"),
        GraphQLImage("image"),
        GraphQLInt("points"),
        GraphQLString("created_at"),
        GraphQLString("updated_at"),
    ]

    main_content_panels = [
        ReadOnlyPanel("id", heading="ID/Activation ID"),
        FieldPanel("collectors"),
        FieldPanel("title"),
        FieldPanel("description"),
        ImageChooserPanel("image"),
        FieldPanel("points"),
        MultiFieldPanel(
            [
                ReadOnlyPanel("created_at", heading="Created"),
                ReadOnlyPanel("updated_at", heading="Updated"),
            ],
            heading="Meta",
        ),
    ]

    edit_handler = TabbedInterface(
        [ObjectList(main_content_panels, heading="Content"),]
    )

    def __str__(self):
        return f"{self.title} ({self.points})"
