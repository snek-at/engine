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

from esite.bifrost.models import (
    GraphQLField,
    GraphQLString,
    GraphQLStreamfield,
)

# Create your homepage related models here.

# > Homepage
class HomePage(Page):
    city = models.CharField(null=True, blank=False, max_length=255)
    zip_code = models.CharField(null=True, blank=False, max_length=255)
    address = models.CharField(null=True, blank=False, max_length=255)
    telephone = models.CharField(null=True, blank=False, max_length=255)
    telefax = models.CharField(null=True, blank=False, max_length=255)
    vat_number = models.CharField(null=True, blank=False, max_length=255)
    whatsapp_telephone = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_contactline = models.CharField(null=True, blank=True, max_length=255)
    tax_id = models.CharField(null=True, blank=False, max_length=255)
    trade_register_number = models.CharField(null=True, blank=False, max_length=255)
    court_of_registry = models.CharField(null=True, blank=False, max_length=255)
    place_of_registry = models.CharField(null=True, blank=False, max_length=255)
    trade_register_number = models.CharField(null=True, blank=False, max_length=255)
    ownership = models.CharField(null=True, blank=False, max_length=255)
    email = models.CharField(null=True, blank=False, max_length=255)

    copyrightholder = models.CharField(null=True, blank=False, max_length=255)

    about = RichTextField(null=True, blank=False)
    privacy = RichTextField(null=True, blank=False)

    sociallinks = StreamField(
        [
            (
                "link",
                blocks.URLBlock(
                    help_text="Important! Format https://www.domain.tld/xyz"
                ),
            )
        ]
    )

    array = []

    def sociallink_company(self):
        for link in self.sociallinks:
            self.array.append(str(link).split(".")[1])
        return self.array

    headers = StreamField(
        [
            (
                "code",
                blocks.RawHTMLBlock(
                    null=True, blank=True, classname="full", icon="code"
                ),
            )
        ],
        null=True,
        blank=False,
    )

    sections = StreamField(
        [
            (
                "code",
                blocks.RawHTMLBlock(
                    null=True, blank=True, classname="full", icon="code"
                ),
            )
        ],
        null=True,
        blank=False,
    )

    token = models.CharField(null=True, blank=True, max_length=255)

    graphql_fields = [
        GraphQLStreamfield("headers"),
        GraphQLStreamfield("sections"),
    ]

    main_content_panels = [StreamFieldPanel("headers"), StreamFieldPanel("sections")]

    imprint_panels = [
        MultiFieldPanel(
            [
                FieldPanel("city"),
                FieldPanel("zip_code"),
                FieldPanel("address"),
                FieldPanel("telephone"),
                FieldPanel("telefax"),
                FieldPanel("whatsapp_telephone"),
                FieldPanel("whatsapp_contactline"),
                FieldPanel("email"),
                FieldPanel("copyrightholder"),
            ],
            heading="contact",
        ),
        MultiFieldPanel(
            [
                FieldPanel("vat_number"),
                FieldPanel("tax_id"),
                FieldPanel("trade_register_number"),
                FieldPanel("court_of_registry"),
                FieldPanel("place_of_registry"),
                FieldPanel("trade_register_number"),
                FieldPanel("ownership"),
            ],
            heading="legal",
        ),
        StreamFieldPanel("sociallinks"),
        MultiFieldPanel(
            [FieldPanel("about"), FieldPanel("privacy")], heading="privacy",
        ),
    ]

    token_panel = [FieldPanel("token")]

    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels + main_content_panels, heading="Main"),
            ObjectList(imprint_panels, heading="Imprint"),
            ObjectList(
                Page.promote_panels + token_panel + Page.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )
