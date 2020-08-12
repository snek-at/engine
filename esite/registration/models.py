import json
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import (
    TabbedInterface,
    ObjectList,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel,
    FieldPanel,
)
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractEmailForm,
    AbstractFormSubmission,
)
from wagtail.admin.mail import send_mail

from esite.bifrost.models import (
    GraphQLInt,
    GraphQLBoolean,
    GraphQLString,
    GraphQLFloat,
    GraphQLImage,
    GraphQLDocument,
    GraphQLSnippet,
    GraphQLEmbed,
    GraphQLStreamfield,
    GraphQLForeignKey,
)
from esite.bifrost.helpers import register_streamfield_block

from esite.bifrost.models import (
    GraphQLForeignKey,
    GraphQLField,
    GraphQLStreamfield,
    GraphQLImage,
    GraphQLString,
    GraphQLCollection,
    GraphQLEmbed,
    GraphQLSnippet,
    GraphQLBoolean,
    GraphQLSnippet,
)
from modelcluster.models import ClusterableModel
from esite.utils.models import BasePage, BaseEmailFormPage
from esite.people.models import PersonFormPage
from esite.redemption.models import Redemption
from esite.profile.models import Profile

# Create your registration related models here.


# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for non-enterprise datasets based on the User model
        return super(ProxyManager, self).get_queryset().filter(is_active=False)


class Registration(get_user_model()):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add Registration form
    # panels = [
    #     FieldPanel("username"),
    #     FieldPanel("is_enterprise"),
    #     FieldPanel("enterprise_id"),
    #     FieldPanel("birthdate"),
    #     FieldPanel("telephone"),
    #     FieldPanel("address"),
    #     FieldPanel("city"),
    #     FieldPanel("postal_code"),
    #     FieldPanel("email"),
    #     FieldPanel("country"),
    #     FieldPanel("newsletter"),
    #     FieldPanel("cache"),
    #     FieldPanel("platform_data"),
    #     FieldPanel("education_data"),
    #     FieldPanel("sources"),
    #     FieldPanel("verified"),
    # ]

    def __str__(self):
        return self.username

    class Meta:
        proxy = True
        ordering = ("date_joined", )


class GitlabServer(ClusterableModel):
    form = ParentalKey("PersonRegistrationFormPage",
                       on_delete=models.CASCADE,
                       related_name="supported_gitlabs")

    organisation = models.CharField(
        null=True,
        max_length=255,
        help_text="The owner of gitlab server.",
    )
    domain = models.URLField(
        null=True,
        max_length=255,
        help_text="The domain of supported gitlab server.",
    )

    graphql_fields = [
        GraphQLString("organisation"),
        GraphQLString("domain"),
    ]


class PersonRegistrationFormField(AbstractFormField):
    page = ParentalKey("PersonRegistrationFormPage",
                       on_delete=models.CASCADE,
                       related_name="form_fields")


class PersonRegistrationFormPage(BaseEmailFormPage):
    template = 'patterns/pages/forms/form_page.html'
    # Only allow creating HomePages at the root level
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "Person Registration Form Page"

    # When creating a new Form page in Wagtail
    registration_head = models.CharField(null=True,
                                         blank=False,
                                         max_length=255)
    registration_newsletter_text = models.CharField(null=True,
                                                    blank=False,
                                                    max_length=255)
    registration_privacy_text = RichTextField(
        null=True,
        blank=False,
    )
    registration_info_text = RichTextField(
        null=True,
        blank=False,
    )
    registration_button = models.ForeignKey(
        "utils.Button",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    registration_step_text = RichTextField(
        null=True,
        blank=False,
    )
    thank_you_text = RichTextField(
        null=True,
        blank=False,
    )

    graphql_fields = [
        GraphQLString("registration_head"),
        GraphQLString("registration_newsletter_text"),
        GraphQLString("registration_privacy_text"),
        GraphQLString("registration_info_text"),
        GraphQLSnippet("registration_button", snippet_model="utils.Button"),
        GraphQLString("registration_step_text"),
        GraphQLString("thank_you_text"),
        GraphQLCollection(GraphQLForeignKey, "supported_gitlabs",
                          "registration.GitlabServer"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("registration_head", classname="full title"),
                FieldPanel("registration_newsletter_text", classname="full"),
                FieldPanel("registration_privacy_text", classname="full"),
                FieldPanel("registration_info_text", classname="full"),
                FieldPanel("registration_step_text", classname="full"),
                SnippetChooserPanel("registration_button", classname="full"),
                FieldPanel("thank_you_text", classname="full"),
                InlinePanel("supported_gitlabs", label="Supported Gitlabs")
            ],
            heading="content",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel("from_address", classname="col6"),
                    FieldPanel("to_address", classname="col6"),
                ]),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")],
            heading="data",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(
            BaseEmailFormPage.content_panels + content_panels,
            heading="Content",
        ),
        ObjectList(
            BaseEmailFormPage.promote_panels +
            BaseEmailFormPage.settings_panels,
            heading="Settings",
            classname="settings",
        ),
    ])

    def get_submission_class(self):
        return PersonRegistrationFormSubmission

    # Create a new user
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email,
        display_email,
        workplace,
        display_workplace,
        job_title,
        website,
        location,
        rank,
        display_ranke,
        display_languages,
        status,
        bio,
        password,
        redemption_code,
        registration_data,
    ):

        # enter the data here
        user = get_user_model()(
            username=username,
            is_active=False,
        )

        user.set_password(password)

        parent_page = Page.objects.get(url_path="/home/people/").specific

        if redemption_code:
            redemption = Redemption.objects.get(pk=f'{redemption_code}')
            if gift.is_active:
                people_page = PersonFormPage(
                    title=f"{user.username}",
                    slug=f"p-{user.username}",
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    display_email=False,
                    workplace="SNEK",
                    display_workplace=False,
                    job_title="CTO",
                    website="https://erebos.xyz",
                    location="@snek",
                    rank="A",
                    status="I am a SNEK",
                    bio="I am a Reptilian",
                )

                redemption.is_active = False

            redemption.save()

        else:
            people_page = PersonFormPage(
                title=f"{user.username}",
                slug=f"p-{user.username}",
                first_name=first_name,
                last_name=last_name,
                email=email,
                display_email=False,
                workplace="SNEK",
                display_workplace=False,
                job_title="CTO",
                website="https://erebos.xyz",
                location="@snek",
                rank="A",
                status="I am a SNEK",
                bio="I am a Reptilian",
            )

        people_page.profiles.add(
            Profile(
                platformName="fff",
                platformUrl="",
                avatarUrl="",
                websiteUrl="",
                company="",
                email="",
                username="",
                fullname="",
                createdAt="",
                location="",
                statusMessage="",
                statusEmojiHTML="",
            ))

        user.save()

        people_page.user = user

        parent_page.add_child(instance=people_page)

        people_page.save_revision().publish()

        return user

    # Called when a user registers
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New registration via Pharmaziegasse Website"

        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            content.append("{}: {}".format(field.label, value))
        content = "\n".join(content)

        content += "\n\nMade with ❤ by a tiny SNEK"

        # emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'

        # html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"

        send_mail(self.subject, f"{emailheader}\n\n{content}", addresses,
                  self.from_address)

    def process_form_submission(self, form):

        user = self.create_user(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            display_email=form.cleaned_data["display_email"],
            workplace=form.cleaned_data["workplace"],
            display_workplace=form.cleaned_data["display_workplace"],
            job_title=form.cleaned_data["job_title"],
            website=form.cleaned_data["website"],
            location=form.cleaned_data["location"],
            rank=form.cleaned_data["rank"],
            display_ranke=form.cleaned_data["display_ranke"],
            display_languages=form.cleaned_data["display_languages"],
            status=form.cleaned_data["status"],
            bio=form.cleaned_data["bio"],
            password=form.cleaned_data["password"],
            redemption_code=form.cleaned_data["redemption_code"],
            registration_data=json.dumps(form.cleaned_data,
                                         cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)


class PersonRegistrationFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class EnterpriseRegistrationFormField(AbstractFormField):
    page = ParentalKey("EnterpriseRegistrationFormPage",
                       on_delete=models.CASCADE,
                       related_name="form_fields")


class EnterpriseRegistrationFormPage(BaseEmailFormPage):
    template = 'patterns/pages/forms/form_page.html'
    # Only allow creating HomePages at the root level
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "Enterprise Registration Form Page"

    # When creating a new Form page in Wagtail
    registration_head = models.CharField(null=True,
                                         blank=False,
                                         max_length=255)
    registration_newsletter_text = models.CharField(null=True,
                                                    blank=False,
                                                    max_length=255)
    registration_privacy_text = RichTextField(
        null=True,
        blank=False,
    )
    registration_info_text = RichTextField(
        null=True,
        blank=False,
    )
    registration_button = models.ForeignKey(
        "utils.Button",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    registration_step_text = RichTextField(
        null=True,
        blank=False,
    )

    thank_you_text = RichTextField(
        null=True,
        blank=False,
    )

    graphql_fields = [
        GraphQLString("registration_head"),
        GraphQLString("registration_newsletter_text"),
        GraphQLString("registration_privacy_text"),
        GraphQLString("registration_info_text"),
        GraphQLSnippet("registration_button", snippet_model="utils.Button"),
        GraphQLString("registration_step_text"),
        GraphQLString("thank_you_text"),
        GraphQLCollection(GraphQLForeignKey, "supported_gitlabs",
                          "registration.GitlabServer"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("registration_head", classname="full title"),
                FieldPanel("registration_newsletter_text", classname="full"),
                FieldPanel("registration_privacy_text", classname="full"),
                FieldPanel("registration_info_text", classname="full"),
                FieldPanel("registration_step_text", classname="full"),
                SnippetChooserPanel("registration_button", classname="full"),
                FieldPanel("thank_you_text", classname="full"),
            ],
            heading="content",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel([
                    FieldPanel("from_address", classname="col6"),
                    FieldPanel("to_address", classname="col6"),
                ]),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")],
            heading="data",
        ),
    ]

    edit_handler = TabbedInterface([
        ObjectList(
            BaseEmailFormPage.content_panels + content_panels,
            heading="Content",
        ),
        ObjectList(
            BaseEmailFormPage.promote_panels +
            BaseEmailFormPage.settings_panels,
            heading="Settings",
            classname="settings",
        ),
    ])

    def get_submission_class(self):
        return EnterpriseRegistrationFormSubmission

    # Create a new user
    def create_user(
        self,
        imprint_tab_name,
        city,
        zip_code,
        address,
        telephone,
        telefax,
        vat_number,
        whatsapp_telephone,
        whatsapp_contactline,
        tax_id,
        trade_register_number,
        court_of_registry,
        place_of_registry,
        ownership,
        email,
        employee_count,
        opensource_url,
        recruiting_url,
        description,
        registration_data,
    ):

        # enter the data here
        user = get_user_model()(
            username=username,
            is_active=False,
        )

        user.set_password(password)

        parent_page = Page.objects.get(url_path="/home/enterprises/").specific

        enterprise_page = PersonFormPage(
            title=f"{user.username}",
            slug=f"e-{user.username}",
            imprint_tab_name=imprint_tab_name,
            city=city,
            zip_code=zip_code,
            address=address,
            telephone=telephone,
            telefax=telefax,
            vat_number=vat_number,
            whatsapp_telephone=whatsapp_telephone,
            whatsapp_contactline=whatsapp_contactline,
            tax_id=tax_id,
            trade_register_number=trade_register_number,
            court_of_registry=court_of_registry,
            place_of_registry=place_of_registry,
            ownership=ownership,
            email=email,
            employee_count=employee_count,
            opensource_url=opensource_url,
            recruiting_url=recruiting_url,
            description=description,
        )

        enterprise_page.profiles.add(
            Profile(
                platformName="fff",
                platformUrl="",
                avatarUrl="",
                websiteUrl="",
                company="",
                email="",
                username="",
                fullname="",
                createdAt="",
                location="",
                statusMessage="",
                statusEmojiHTML="",
                bids="",
                tids="",
            ))

        user.save()

        enterprise_page.user = user

        parent_page.add_child(instance=enterprise_page)

        enterprise_page.save_revision().publish()

        return user

    # Called when a user registers
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New registration via Pharmaziegasse Website"

        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            content.append("{}: {}".format(field.label, value))
        content = "\n".join(content)

        content += "\n\nMade with ❤ by a tiny SNEK"

        # emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'

        # html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"

        send_mail(self.subject, f"{emailheader}\n\n{content}", addresses,
                  self.from_address)

    def process_form_submission(self, form):

        user = self.create_user(
            imprint_tab_name=form.cleaned_data["imprint_tab_name"],
            city=form.cleaned_data["city"],
            zip_code=form.cleaned_data["zip_code"],
            address=form.cleaned_data["address"],
            telephone=form.cleaned_data["telephone"],
            telefax=form.cleaned_data["telefax"],
            vat_number=form.cleaned_data["vat_number"],
            whatsapp_telephone=form.cleaned_data["whatsapp_telephone"],
            whatsapp_contactline=form.cleaned_data["whatsapp_contactline"],
            tax_id=form.cleaned_data["tax_id"],
            trade_register_number=form.cleaned_data["trade_register_number"],
            court_of_registry=form.cleaned_data["court_of_registry"],
            place_of_registry=form.cleaned_data["place_of_registry"],
            ownership=form.cleaned_data["ownership"],
            email=form.cleaned_data["email"],
            employee_count=form.cleaned_data["employee_count"],
            opensource_url=form.cleaned_data["opensource_url"],
            recruiting_url=form.cleaned_data["recruiting_url"],
            description=form.cleaned_data["description"],
            registration_data=json.dumps(form.cleaned_data,
                                         cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)


class EnterpriseRegistrationFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
