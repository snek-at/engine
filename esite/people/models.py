from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
from wagtail.core.fields import StreamField
from wagtail.images import get_image_model
from wagtail.images.edit_handlers import ImageChooserPanel

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
from esite.utils.models import BaseFormPage, BasePage


class SocialMediaProfile(models.Model):
    person_page = ParentalKey("PersonFormPage", related_name="social_media_profile")
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


class Person(ClusterableModel):
    user = ParentalKey(
        "user.SNEKUser", on_delete=models.CASCADE, related_name="person"
    )
    sources = models.TextField(null=True, blank=False)
    cache = models.TextField(null=True, blank=False)
    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        FieldPanel("sources"),
        FieldPanel("cache"),
        InlinePanel("person_page", label="Person Page"),
    ]

    graphql_fields = [
        GraphQLString("user"),
        GraphQLString("sources"),
        GraphQLString("cache"),
        GraphQLCollection(GraphQLForeignKey, "person_page", "people.PersonFormPage"),
    ]

    def __str__(self):
        return user.username


class PersonFormField(AbstractFormField):
    page = ParentalKey(
        "PersonFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class PersonFormPage(BaseFormPage):
    template = "patterns/pages/people/person_page.html"

    parent_page_types = ["people.PersonIndex"]
    subpage_types = []

    show_in_menus_default = False

    class Meta:
        verbose_name = "Person Form Page"

    person = ParentalKey(
        "Person", on_delete=models.CASCADE, related_name="person_page"
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ForeignKey(
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
    job_title = models.CharField(blank=True, max_length=255)
    website = models.CharField(blank=True, max_length=255)
    location = models.CharField(blank=True, max_length=255)
    rank = models.CharField(blank=True, max_length=1)
    display_rank = models.BooleanField(blank=True, default=False)
    display_languages = models.BooleanField(blank=True, default=False)
    status = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    bids = models.TextField(null=True, blank=True)
    tids = models.TextField(null=True, blank=True)

    follows = models.ManyToManyField("PersonFormPage", null=True, related_name="followed_by")
    likes = models.ManyToManyField("PersonFormPage", null=True, related_name="liked_by")

    content_panels = BasePage.content_panels + [
        FieldPanel("person"),
        MultiFieldPanel(
            [FieldPanel("first_name"), FieldPanel("last_name"),], heading="Name"
        ),
        ImageChooserPanel("photo"),
        FieldPanel("workplace"),
        FieldPanel("display_workplace"),
        FieldPanel("job_title"),
        InlinePanel("social_media_profile", label="Social accounts"),
        InlinePanel("profiles", label="Profiles"),
        MultiFieldPanel(
            [FieldPanel("email"), FieldPanel("display_email"),],
            heading="Contact information",
        ),
        FieldPanel("website"),
        FieldPanel("rank"),
        FieldPanel("display_rank"),
        FieldPanel("display_languages"),
        FieldPanel("status"),
        FieldPanel("bio"),
        FieldPanel("location"),
        FieldPanel("bids"),
        FieldPanel("tids"),
    ]

    form_panels = [
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")], heading="data",
        ),
    ]

    social_panel = [
        MultiFieldPanel([FieldPanel("follows")], heading="Followings",),
        # MultiFieldPanel([FieldPanel("achievements")], heading="Achievements",),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(social_panel, heading="Social"),
            ObjectList(form_panels, heading="Form"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("job_title"),
        GraphQLString("status"),
        GraphQLImage("photo"),
        GraphQLStreamfield("bio"),
        GraphQLString("bids"),
        GraphQLString("tids"),
        GraphQLCollection(GraphQLForeignKey, "follows", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "followed_by", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "likes", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "liked_by", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "achievements", "achievement.Achievement"),
        GraphQLCollection(GraphQLForeignKey, "profiles", "profile.Profile"),
    ]


class PersonIndex(BasePage):
    template = "patterns/pages/people/person_index_page.html"

    # Only allow creating HomePages at the root level
    parent_page_types = ["home.HomePage"]
    subpage_types = ["PersonFormPage"]

    class Meta:
        verbose_name = "Person Index"

    def get_context(self, request, *args, **kwargs):
        people = (
            PersonFormPage.objects.live().public().descendant_of(self).order_by("slug")
        )

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
