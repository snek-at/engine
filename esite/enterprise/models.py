import uuid
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
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
    AbstractEmailForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from wagtail.contrib.forms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractEmailForm,
    AbstractFormSubmission,
)
from modelcluster.fields import ParentalKey
from esite.utils.models import BasePage, BaseEmailFormPage
from esite.bifrost.helpers import register_streamfield_block
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
)
from esite.colorfield.blocks import ColorBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import fields

# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for activate enterprise datasets based on the User model
        return super(ProxyManager, self).get_queryset().filter(is_enterprise=True)


class Enterprise(get_user_model()):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("is_enterprise"),
        FieldPanel("date_joined"),
        # FieldPanel('title'),
        # FieldPanel('first_name'),
        # FieldPanel('last_name'),
        # FieldPanel('email'),
        # FieldPanel('telephone'),
        # FieldPanel('address'),
        # FieldPanel('zipCode'),
        # FieldPanel('city'),
        # FieldPanel('country'),
        # FieldPanel('newsletter'),
        # FieldPanel('cache'),
    ]

    def __str__(self):
        return self.username

    class Meta:
        proxy = True
        ordering = ("date_joined",)


# > Overview Section
@register_streamfield_block
class _S_OverviewBlock(blocks.StructBlock):
    # feed = blocks.StreamBlock(
    #     [("feed", Overview_FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
    #     null=True,
    #     blank=False,
    # )
    # total contribs of all projects
    # statistic of past and current week
    # statistic of al lyears # current
    # source code statistic language
    # source code statistic lines of code
    pass


#  "commit": "e5ab38813bfc2bb100352adcf525a98caf396411",
#       "author": "Administrator \u003cadmin@example.com\u003e",
#       "date": "Thu Jul 30 11:15:12 2020 +0000",
#       "message": "Update-.gitlab-ci.yml",
#       "files": [
#         {
#           "insertions": "1",
#           "deletions": "1",
#           "path": ".gitlab-ci.yml",
#           "raw_changes": "\u001b[31m-    paths: [log.log]\u001b[m\n\u001b[32m+\u001b[m\u001b[32m    paths: [tmp.json]\u001b[m\n"
#         }
#       ]


@register_streamfield_block
class CodeStatisticLanguageBlock(blocks.StructBlock):
    language_name = blocks.CharBlock()
    color = ColorBlock()
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()

    graphql_fields = [
        GraphQLString("language_name"),
        GraphQLString("color"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
    ]


@register_streamfield_block
class CodeStatisticBlock(blocks.StructBlock):
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()
    date = blocks.DateTimeBlock()

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("date"),
    ]


@register_streamfield_block
class FeedCommitFileBlock(blocks.StructBlock):
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()
    path = blocks.CharBlock()
    raw_changes = blocks.TextBlock()

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("path"),
        GraphQLString("raw_changes"),
    ]


@register_streamfield_block
class FeedCommitBlock(blocks.StructBlock):
    contribution_id = blocks.CharBlock()
    date = blocks.DateTimeBlock()
    message = blocks.TextBlock()
    files = blocks.StreamBlock(
        [("file", FeedCommitFileBlock(null=True, blank=True, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("contribution_id"),
        GraphQLString("date"),
        GraphQLString("message"),
        GraphQLStreamfield("files"),
    ]


@register_streamfield_block
class FeedBlock(blocks.StructBlock):
    datetime = blocks.DateTimeBlock(null=True, required=True)
    data = blocks.StreamBlock(
        [
            ("commit", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("issue", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("pr", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("review", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("contribution_id"),
        GraphQLStreamfield("data"),
    ]


@register_streamfield_block
class _S_ScpPageUser(blocks.StructBlock):
    name = blocks.CharBlock()
    username = blocks.CharBlock()
    active = blocks.BooleanBlock(default=False)
    avatar = ImageChooserBlock()
    feed = blocks.StreamBlock(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )
    history = blocks.StreamBlock(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )

    languages = blocks.StreamBlock(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLString("active"),
        GraphQLString("avatar"),
        GraphQLStreamfield("feed"),
        GraphQLStreamfield("history"),
        GraphQLStreamfield("languages"),
    ]


@register_streamfield_block
class _S_ProjectBlock(blocks.StructBlock):
    name = blocks.CharBlock(null=True, required=True, help_text="Project name")
    url = blocks.URLBlock(
        null=True,
        required=True,
        help_text="Important! Format https://www.domain.tld/xyz",
    )
    description = blocks.TextBlock(
        null=True, required=False, help_text="Project description"
    )

    maintainer_name = blocks.CharBlock()
    maintainer_username = blocks.CharBlock()
    maintainer_email = blocks.EmailBlock()

    contributors = blocks.StreamBlock(
        [("contributor", _S_ScpPageUser(null=True, blank=False, icon="fa-user"),)]
    )

    feed = blocks.StreamBlock(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )

    history = blocks.StreamBlock(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )

    languages = blocks.StreamBlock(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("url"),
        GraphQLString("description"),
        GraphQLString("maintainer_name"),
        GraphQLString("maintainer_username"),
        GraphQLString("maintainer_email"),
        GraphQLStreamfield("contributors"),
        GraphQLStreamfield("feed"),
        GraphQLStreamfield("history"),
        GraphQLStreamfield("languages"),
    ]


# > Pages
class EnterpriseFormField(AbstractFormField):
    page = ParentalKey(
        "EnterpriseFormPage", on_delete=models.CASCADE, related_name="form_fields"
    )

class EnterpriseFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class EnterpriseFormPage(BaseEmailFormPage):
    # Only allow creating HomePages at the root level
    parent_page_types = ["EnterpriseIndex"]
    graphql_fields = []

    """[Tabs]
    
    Wagtail content and API definition of all tabs
    """
    # Overview
    overview_tab_name = models.CharField(null=True, blank=True, max_length=255)
    feed_section = fields.StreamField(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )
    history_section = fields.StreamField(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )
    languages_section = fields.StreamField(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    overview_panels = [
        FieldPanel("overview_tab_name"),
        StreamFieldPanel("feed_section"),
        StreamFieldPanel("history_section"),
        StreamFieldPanel("languages_section"),
    ]

    graphql_fields += [
        GraphQLString("overview_tab_name"),
        GraphQLStreamfield("feed_section"),
        GraphQLStreamfield("history_section"),
        GraphQLStreamfield("languages_section"),
    ]

    # Users
    users_tab_name = models.CharField(null=True, blank=True, max_length=255)
    users_section = fields.StreamField(
        [("S_UserBlock", _S_ScpPageUser(null=True, icon="cogs")),],
        null=True,
        blank=True,
    )

    user_panels = [FieldPanel("users_tab_name"), StreamFieldPanel("users_section")]
    # Projects
    project_tab_name = models.CharField(null=True, blank=True, max_length=255)
    projects_section = fields.StreamField(
        [("S_ProjectBlock", _S_ProjectBlock(null=True, icon="cogs")),],
        null=True,
        blank=True,
    )

    project_panels = [
        FieldPanel("project_tab_name"),
        StreamFieldPanel("projects_section"),
    ]

    graphql_fields += [
        GraphQLString("project_tab_name"),
        GraphQLStreamfield("projects_section"),
    ]

    # Imprint
    imprint_tab_name = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    zip_code = models.CharField(null=True, blank=True, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    telephone = models.CharField(null=True, blank=True, max_length=255)
    telefax = models.CharField(null=True, blank=True, max_length=255)
    vat_number = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_telephone = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_contactline = models.CharField(null=True, blank=True, max_length=255)
    tax_id = models.CharField(null=True, blank=True, max_length=255)
    trade_register_number = models.CharField(null=True, blank=True, max_length=255)
    court_of_registry = models.CharField(null=True, blank=True, max_length=255)
    place_of_registry = models.CharField(null=True, blank=True, max_length=255)
    trade_register_number = models.CharField(null=True, blank=True, max_length=255)
    ownership = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    employee_count = models.CharField(null=True, blank=True, max_length=255)
    opensource_url = models.URLField(null=True, blank=True)
    recruiting_url = models.URLField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)

    imprint_panels = [
        FieldPanel("imprint_tab_name"),
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
        MultiFieldPanel(
            [
                FieldPanel("employee_count"),
                FieldPanel("opensource_url"),
                FieldPanel("recruiting_url"),
                FieldPanel("description"),
            ],
            heading="about",
        ),
    ]

    graphql_fields += [
        GraphQLString("imprint_tab_name"),
        GraphQLString("city"),
        GraphQLString("zip_code"),
        GraphQLString("address"),
        GraphQLString("telephone"),
        GraphQLString("telefax"),
        GraphQLString("vat_number"),
        GraphQLString("whatsapp_telephone"),
        GraphQLString("whatsapp_contactline"),
        GraphQLString("tax_id"),
        GraphQLString("trade_register_number"),
        GraphQLString("court_of_registry"),
        GraphQLString("place_of_registry"),
        GraphQLString("trade_register_number"),
        GraphQLString("ownership"),
        GraphQLString("email"),
        GraphQLString("employee_count"),
        GraphQLString("opensource_url"),
        GraphQLString("recruiting_url"),
        GraphQLString("description"),
    ]
    # Settings
    settings_tab_name = models.CharField(null=True, blank=True, max_length=255)
    cache = models.TextField(null=True, blank=True)

    cache_panels = [FieldPanel("cache")]
    form_panels = [
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

    graphql_fields += [
        GraphQLString("cache"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels + overview_panels, heading="Overview"),
            ObjectList(user_panels, heading="Users"),
            ObjectList(project_panels, heading="Projects"),
            ObjectList(imprint_panels, heading="Imprint"),
            ObjectList(form_panels, heading="Form"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels + cache_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    def get_submission_class(self):
        return RegistrationFormSubmission

    # Create a new user
    def create_enterprise_user(
        cache,
    ):
        # enter the data here
        user = get_user_model()(
            username="anexia",
            is_enterprise=True,
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

        user = self.create_enterprise_user(
            cache=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)



class EnterpriseIndex(BasePage):
    #template = 'patterns/pages/enterprise/person_index_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ['EnterpriseFormPage']

    def get_context(self, request, *args, **kwargs):
        enterprise = EnterpriseFormPage.objects.live().public().descendant_of(self).order_by('slug')

        page_number = request.GET.get('page', 1)
        paginator = Paginator(enterprise, settings.DEFAULT_PER_PAGE)
        try:
            enterprise = paginator.page(page_number)
        except PageNotAnInteger:
            enterprise = paginator.page(1)
        except EmptyPage:
            enterprise = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(enterprise=enterprise)

        return context