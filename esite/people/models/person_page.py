from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images import get_image_model
from wagtail.images.edit_handlers import ImageChooserPanel

from esite.bifrost.helpers import register_streamfield_block
from esite.bifrost.models import (
    GraphQLBoolean,
    GraphQLCollection,
    GraphQLDocument,
    GraphQLEmbed,
    GraphQLFloat,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLInt,
    GraphQLSnippet,
    GraphQLStreamfield,
    GraphQLString,
)

# from esite.utils.blocks import StoryBlock
from esite.profile.models import Profile
from esite.utils.models import BaseFormPage, BasePage


@register_streamfield_block
class Movable(blocks.StructBlock):
    order = blocks.ListBlock(blocks.IntegerBlock())

    graphql_fields = [GraphQLStreamfield("order")]


class SocialMediaProfile(models.Model):
    person_page = ParentalKey("PersonPage", related_name="social_media_profile")
    site_titles = (("twitter", "Twitter"), ("linkedin", "LinkedIn"))
    site_urls = (
        ("twitter", "https://twitter.com/"),
        ("linkedin", "https://www.linkedin.com/in/"),
    )
    service = models.CharField(max_length=200, choices=site_titles)
    username = models.CharField(max_length=255)

    @property
    def profile_url(self):
        return dict(self.site_urls)[self.service] + self.username

    def clean(self):
        if self.service == "twitter" and self.username.startswith("@"):
            self.username = self.username[1:]


class Meta_Link(models.Model):
    LINK_TYPES = (
        ("INSTAGRAM", "Instagram Post"),
        ("PHOTO", "Photo URL"),
        ("YOUTUBE", "Youtube URL"),
        ("VIMEO", "VIMEO URL"),
        ("OTHER", "Other"),
    )
    person_page = ParentalKey("PersonPage", related_name="meta_links")
    url = models.URLField(max_length=255)
    link_type = models.CharField(choices=LINK_TYPES, default="OTHER", max_length=255)

    # > Meta
    location = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    imgur_delete_hash = models.CharField(null=True, blank=True, max_length=255)

    graphql_fields = [
        GraphQLString("url"),
        GraphQLString("link_type"),
        GraphQLString("location"),
        GraphQLString("description"),
        GraphQLString("imgur_delete_hash"),
    ]


class PersonPage(BasePage):
    template = "patterns/pages/people/person_page.html"

    parent_page_types = ["people.PersonIndex"]
    subpage_types = []

    show_in_menus_default = False

    class Meta:
        verbose_name = "Person Page"

    person = models.OneToOneField(
        "Person", on_delete=models.CASCADE, related_name="person_page"
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    status = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    avatar_image = models.ForeignKey(
        settings.WAGTAILIMAGES_IMAGE_MODEL,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    email = models.EmailField(blank=True)
    display_email = models.BooleanField(blank=True, default=False)
    workplace = models.CharField(blank=True, max_length=255)
    display_workplace = models.BooleanField(blank=True, default=False)
    website_url = models.URLField(blank=True, max_length=255)
    location = models.CharField(blank=True, max_length=255)
    display_ranking = models.BooleanField(blank=True, default=False)
    display_programming_languages = models.BooleanField(blank=True, default=False)
    display_2d_calendar = models.BooleanField(blank=True, default=False)
    display_3d_calendar = models.BooleanField(blank=True, default=False)

    bids = models.TextField(null=True, blank=True)
    tids = models.TextField(null=True, blank=True)

    follows = models.ManyToManyField(
        "PersonPage", null=True, blank=True, related_name="followed_by"
    )
    likes = models.ManyToManyField(
        "PersonPage", null=True, blank=True, related_name="liked_by"
    )

    movable_pool = StreamField(
        [("overview", Movable()), ("contribtype", Movable())], null=True, blank=True,
    )

    content_panels = BasePage.content_panels + [
        FieldPanel("person"),
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name"),], heading="Name"
        ),
        ImageChooserPanel("avatar_image"),
        FieldPanel("workplace"),
        FieldPanel("display_workplace"),
        InlinePanel("social_media_profile", label="Social accounts"),
        InlinePanel("profiles", label="Profiles"),
        InlinePanel("meta_links", label="Meta Links"),
        MultiFieldPanel(
            [FieldPanel("email"), FieldPanel("display_email"),],
            heading="Contact information",
        ),
        FieldPanel("website_url"),
        FieldPanel("display_ranking"),
        FieldPanel("display_programming_languages"),
        FieldPanel("display_2d_calendar"),
        FieldPanel("display_3d_calendar"),
        FieldPanel("status"),
        FieldPanel("bio"),
        FieldPanel("location"),
        FieldPanel("bids"),
        FieldPanel("tids"),
        StreamFieldPanel("movable_pool"),
    ]

    social_panel = [
        MultiFieldPanel([FieldPanel("follows")], heading="Followings",),
        # MultiFieldPanel([FieldPanel("achievements")], heading="Achievements",),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(social_panel, heading="Social"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    graphql_fields = [
        GraphQLString("title", required=True),
        GraphQLString("first_name"),
        GraphQLString("last_name"),
        GraphQLString("status"),
        GraphQLString("bio"),
        GraphQLImage("avatar_image"),
        GraphQLString("email"),
        GraphQLBoolean("display_email"),
        GraphQLString("workplace"),
        GraphQLBoolean("display_workplace"),
        GraphQLString("website_url"),
        GraphQLString("location"),
        GraphQLBoolean("display_ranking"),
        GraphQLBoolean("display_programming_languages"),
        GraphQLBoolean("display_2d_calendar"),
        GraphQLBoolean("display_3d_calendar"),
        GraphQLString("bids"),
        GraphQLString("tids"),
        GraphQLStreamfield("movable_pool"),
        GraphQLForeignKey("person", "people.Person"),
        GraphQLCollection(GraphQLForeignKey, "meta_links", "people.Meta_Link"),
        GraphQLCollection(GraphQLForeignKey, "follows", "people.PersonPage"),
        GraphQLCollection(GraphQLForeignKey, "followed_by", "people.PersonPage"),
        GraphQLCollection(GraphQLForeignKey, "likes", "people.PersonPage"),
        GraphQLCollection(GraphQLForeignKey, "liked_by", "people.PersonPage"),
        GraphQLCollection(GraphQLForeignKey, "achievements", "achievement.Achievement"),
        GraphQLCollection(GraphQLForeignKey, "talks", "talk.Talk"),
    ]


class PersonIndex(BasePage):
    template = "patterns/pages/people/person_index_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["home.HomePage"]
    subpage_types = ["PersonPage"]

    class Meta:
        verbose_name = "Person Index"

    def get_context(self, request, *args, **kwargs):
        people = PersonPage.objects.live().public().descendant_of(self).order_by("slug")

        page_number = request.GET.get("page", 1)
        paginator = Paginator(people, settings.DEFAULT_PER_PAGE)
        try:
            people = paginator.page(page_number)
        except PageNotAnInteger:
            people = paginator.page(1)
        except EmptyPage:
            people = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(people=people)

        return context
