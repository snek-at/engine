from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey
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
from wagtail.core.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from esite.bifrost.models import GraphQLField, GraphQLStreamfield, GraphQLString
from esite.colorfield.blocks import ColorAlphaBlock, ColorBlock, GradientColorBlock
from esite.colorfield.fields import ColorAlphaField, ColorField
from esite.utils.models import BasePage

# Create your homepage related models here.

# class HomePageFeaturedPage(Orderable):
#     page = ParentalKey(
#         'home.HomePage',
#         related_name='featured_pages'
#     )
#     featured_page = models.ForeignKey(
#         'person.PersonPage',
#         related_name='+',
#         on_delete=models.CASCADE,
#         verbose_name='featured page',
#     )
#     title = models.CharField(null=True, blank=True, max_length=80)
#     summary = models.TextField(null=True, blank=True, max_length=200)
#     image = models.ForeignKey(
#         'images.SNEKImage',
#         null=True,
#         blank=True,
#         related_name='+',
#         on_delete=models.SET_NULL,
#     )

#     panels = [
#         PageChooserPanel('featured_page'),
#         FieldPanel('title'),
#         FieldPanel('summary'),
#         ImageChooserPanel('image')
#     ]

# > Homepage
class HomePage(BasePage):

    template = "patterns/pages/home/home_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    # subpage_types = []

    class Meta:
        verbose_name = "Home Page"

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

    # headers = StreamField(
    #     [
    #         (
    #             "code",
    #             blocks.RawHTMLBlock(
    #                 null=True, blank=True, classname="full", icon="code"
    #             ),
    #         )
    #     ],
    #     null=True,
    #     blank=False,
    # )

    # sections = StreamField(
    #     [
    #         (
    #             "code",
    #             blocks.RawHTMLBlock(
    #                 null=True, blank=True, classname="full", icon="code"
    #             ),
    #         )
    #     ],
    #     null=True,
    #     blank=False,
    # )

    # token = models.CharField(null=True, blank=True, max_length=255)

    hero_title = models.CharField(null=True, blank=False, max_length=80)

    hero_introduction = models.CharField(null=True, blank=False, max_length=255)

    hero_button_text = models.CharField(null=True, blank=True, max_length=55)

    hero_button_link = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    featured_image = models.ForeignKey(
        "images.SNEKImage",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    # search_fields = BasePage.search_fields + [
    #     index.SearchField('hero_introduction'),
    # ]

    articles_title = models.CharField(null=True, blank=True, max_length=150)
    articles_link = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    articles_linktext = models.CharField(null=True, blank=True, max_length=80)

    featured_pages_title = models.CharField(null=True, blank=True, max_length=150)
    pages_link = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    pages_linktext = models.CharField(null=True, blank=True, max_length=80)

    news_title = models.CharField(null=True, blank=True, max_length=150)
    news_link = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    news_linktext = models.CharField(null=True, blank=True, max_length=80)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["articles_title"] = self.articles_title
        context["articles_link"] = self.articles_link
        context["articles_linktext"] = self.articles_linktext
        context["featured_pages_title"] = self.featured_pages_title
        context["pages_link"] = self.pages_link
        context["pages_linktext"] = self.pages_linktext
        context["news_title"] = self.news_title
        context["news_link"] = self.news_link
        context["news_linktext"] = self.news_linktext

        return context

    content_panels = BasePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_introduction"),
                FieldPanel("hero_button_text"),
                PageChooserPanel("hero_button_link"),
                ImageChooserPanel("featured_image"),
            ],
            heading="Hero Section",
        ),
        # InlinePanel(
        #     'featured_pages',
        #     label="Featured Pages",
        #     max_num=6,
        #     heading='Featured Pages, Maximum 6'
        # ),
        MultiFieldPanel(
            [
                FieldPanel("articles_title"),
                PageChooserPanel("articles_link"),
                FieldPanel("featured_pages_title"),
                PageChooserPanel("pages_link"),
                FieldPanel("news_title"),
                PageChooserPanel("news_link"),
            ],
            heading="Front page sections",
        ),
    ]

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

    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels + content_panels, heading="Content"),
            ObjectList(imprint_panels, heading="Imprint"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )
