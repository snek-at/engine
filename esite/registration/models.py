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

from esite.utils.models import BasePage, BaseEmailFormPage

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
        ordering = ("date_joined",)


@register_streamfield_block
class Gitlab_Server(blocks.StructBlock):
    organisation = blocks.CharBlock(
        null=True,
        blank=False,
        classname="full title",
        help_text="The owner of gitlab server.",
    )
    domain = blocks.CharBlock(
        null=True,
        blank=False,
        classname="full title",
        help_text="The domain of supported gitlab server.",
    )

    graphql_fields = [
        GraphQLString("organisation"),
        GraphQLString("domain"),
    ]


class RegistrationFormField(AbstractFormField):
    page = ParentalKey(
        "RegistrationFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class RegistrationFormPage(BaseEmailFormPage):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = []


    class Meta:
        verbose_name = "Registration Form Page"

    # When creating a new Form page in Wagtail
    registration_head = models.CharField(null=True, blank=False, max_length=255)
    registration_newsletter_text = models.CharField(
        null=True, blank=False, max_length=255
    )
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

    supported_gitlabs = StreamField(
        [("gitlab_server", Gitlab_Server(null=True, blank=False, icon="home")),],
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
        GraphQLStreamfield("supported_gitlabs"),
    ]

    main_content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("registration_head", classname="full title"),
                FieldPanel("registration_newsletter_text", classname="full"),
                FieldPanel("registration_privacy_text", classname="full"),
                FieldPanel("registration_info_text", classname="full"),
                FieldPanel("registration_step_text", classname="full"),
                SnippetChooserPanel("registration_button", classname="full"),
                FieldPanel("thank_you_text", classname="full"),
                StreamFieldPanel("supported_gitlabs"),
            ],
            heading="content",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")], heading="data",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                AbstractEmailForm.content_panels + main_content_panels,
                heading="Content",
            ),
            ObjectList(
                AbstractEmailForm.promote_panels + AbstractEmailForm.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    def get_submission_class(self):
        return RegistrationFormSubmission

    # Create a new user
    def create_user(
        self,
        username,
        telephone,
        address,
        city,
        postal_code,
        email,
        country,
        newsletter,
        platform_data,
        sources,
        verified,
        first_name,
        last_name,
        password,
        cache,
        gift_code,
    ):
        # enter the data here
        user = get_user_model()(
            username=username,
            is_enterprise=False,
            is_active=False,
            cache=cache,
        )

        user.set_password(password)

        user.save()

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

        send_mail(
            self.subject, f"{emailheader}\n\n{content}", addresses, self.from_address
        )

    def process_form_submission(self, form):

        user = self.create_user(
            username=form.cleaned_data["username"],
            telephone=form.cleaned_data["telephone"],
            address=form.cleaned_data["address"],
            city=form.cleaned_data["city"],
            postal_code=form.cleaned_data["postal_code"],
            email=form.cleaned_data["email"],
            country=form.cleaned_data["country"],
            newsletter=form.cleaned_data["newsletter"],
            platform_data=form.cleaned_data["platform_data"],
            sources=form.cleaned_data["sources"],
            verified=form.cleaned_data["verified"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            password=form.cleaned_data["password"],
            gift_code=form.cleaned_data["gift_code"],
            cache=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)


class RegistrationFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
