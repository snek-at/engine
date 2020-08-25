from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core import blocks
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
class Meta_Link(blocks.StructBlock):
    LINK_TYPES = (
        ("instagram_video", "Instagram Post Video"),
        ("instagram_photo", "Instagram Post Photo"),
        ("other", "Other"),
    )

    url = blocks.URLBlock(null=True, blank=True, max_length=255)
    link_type = blocks.ChoiceBlock(choices=LINK_TYPES, default="other")

    # > Meta
    location = blocks.CharBlock(null=True, blank=True, max_length=255)
    description = blocks.TextBlock(null=True, blank=True)


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
    user = ParentalKey("user.SNEKUser", on_delete=models.CASCADE, related_name="person")
    # sources = models.TextField(null=True, blank=False)
    # cache = models.TextField(null=True, blank=False)
    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        # FieldPanel("sources"),
        # FieldPanel("cache"),
    ]

    graphql_fields = [
        GraphQLString("user"),
        # GraphQLString("sources"),
        # GraphQLString("cache"),
    ]

    def __str__(self):
        return self.user.username


class PersonFormField(AbstractFormField):
    page = ParentalKey(
        "PersonFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class PersonFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class PersonFormPage(BaseFormPage):
    template = "patterns/pages/people/person_page.html"

    parent_page_types = ["people.PersonIndex"]
    subpage_types = []

    show_in_menus_default = False

    class Meta:
        verbose_name = "Person Form Page"

    person = models.OneToOneField(
        "Person", on_delete=models.CASCADE, related_name="person_page"
    )

    """[Temporary]
    """
    sources = models.TextField(null=True, blank=False)
    cache = models.TextField(null=True, blank=False)

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

    follows = models.ManyToManyField(
        "PersonFormPage", null=True, blank=True, related_name="followed_by"
    )
    likes = models.ManyToManyField(
        "PersonFormPage", null=True, blank=True, related_name="liked_by"
    )

    link_collection = StreamField([("link", Meta_Link())], null=True, blank=True)

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
        StreamFieldPanel("link_collection"),
        # > Temporary
        FieldPanel("cache"),
        FieldPanel("sources"),
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
        GraphQLString("title", required=True),
        GraphQLString("first_name"),
        GraphQLString("last_name"),
        GraphQLString("email"),
        GraphQLString("job_title"),
        GraphQLString("status"),
        GraphQLImage("photo"),
        GraphQLStreamfield("bio"),
        GraphQLStreamfield("link_collection"),
        GraphQLString("bids"),
        GraphQLString("tids"),
        GraphQLForeignKey("person", "people.Person"),
        # > Temporary
        GraphQLString("cache"),
        GraphQLString("sources"),
        #
        GraphQLCollection(GraphQLForeignKey, "follows", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "followed_by", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "likes", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "liked_by", "people.PersonFormPage"),
        GraphQLCollection(GraphQLForeignKey, "achievements", "achievement.Achievement"),
    ]

    def get_submission_class(self):
        return PersonFormSubmission

    def store_merged_profiles(self, **kwargs):
        print("Merged profile data", **kwargs)
        self.person.save()

    def process_form_submission(self, form):
        self.store_merged_profiles(
            # platformName=form.cleaned_data["platform_name"]
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )


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
