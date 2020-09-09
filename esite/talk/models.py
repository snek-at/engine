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
from esite.utils.edit_handlers import ReadOnlyPanel
from esite.utils.models import BasePage, TimeStampMixin

# Create your homepage related models here.


class Talk(TimeStampMixin, ClusterableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = ParentalKey(
        "people.PersonPage", on_delete=models.CASCADE, related_name="talks"
    )
    title = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(null=True, blank=True, help_text="Other information")
    path = models.CharField(null=True, blank=True, max_length=256)
    url = models.URLField(
        null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz"
    )
    display_url = models.URLField(
        null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz"
    )
    download_url = models.URLField(
        null=True, blank=True, help_text="Important! Format https://www.domain.tld/xyz"
    )

    graphql_fields = [
        GraphQLString("id"),
        GraphQLString("title"),
        GraphQLString("description"),
        GraphQLString("path"),
        GraphQLString("url"),
        GraphQLString("display_url"),
        GraphQLString("download_url"),
        GraphQLString("created_at"),
        GraphQLString("updated_at"),
        GraphQLForeignKey("owner", content_type="people.PersonPage"),
        GraphQLCollection(GraphQLForeignKey, "talk_comments", "comment.Comment"),
    ]

    main_content_panels = [
        ReadOnlyPanel("id", heading="ID"),
        FieldPanel("owner"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("path"),
        FieldPanel("url"),
        FieldPanel("display_url"),
        FieldPanel("download_url"),
        MultiFieldPanel(
            [
                ReadOnlyPanel("created_at", heading="Created"),
                ReadOnlyPanel("updated_at", heading="Updated"),
            ],
            heading="Meta",
        ),
        InlinePanel("talk_comments", label="Comments"),
    ]

    edit_handler = TabbedInterface(
        [ObjectList(main_content_panels, heading="Content"),]
    )
