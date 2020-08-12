import uuid
import json
import os
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
from wagtail.admin.mail import send_mail
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
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
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
    GraphQLCollection,
    GraphQLForeignKey,
)
from esite.colorfield.blocks import ColorBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import fields
import yaml


# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for activate enterprise datasets based on the User model
        return super(ProxyManager,
                     self).get_queryset().filter(is_enterprise=True)


class Enterprise(get_user_model()):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add enterprise form
    # panels = [
    #     FieldPanel("is_enterprise"),
    #     FieldPanel("date_joined"),
    #     # FieldPanel('title'),
    #     # FieldPanel('first_name'),
    #     # FieldPanel('last_name'),
    #     # FieldPanel('email'),
    #     # FieldPanel('telephone'),
    #     # FieldPanel('address'),
    #     # FieldPanel('zipCode'),
    #     # FieldPanel('city'),
    #     # FieldPanel('country'),
    #     # FieldPanel('newsletter'),
    #     # FieldPanel('cache'),
    # ]

    def __str__(self):
        return self.username

    class Meta:
        proxy = True
        ordering = ("date_joined", )


# > Models
class ContributionFeed(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_contribution_feed",
        on_delete=models.SET_NULL,
        null=True,
    )
    type = models.CharField(null=True, max_length=255)
    cid = models.CharField(null=True, max_length=255)
    datetime = models.DateTimeField(null=True)
    message = models.CharField(null=True, max_length=255)
    files = ParentalManyToManyField("ContributionFile",
                                    related_name="files",
                                    null=True,
                                    blank=True)
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic",
        related_name="contributionfeed_codelanguages",
        blank=True,
    )

    graphql_fields = [
        GraphQLForeignKey("page", content_type="enterprises.Contributor"),
        GraphQLString("type"),
        GraphQLString("cid"),
        GraphQLString("datetime"),
        GraphQLString("message"),
        GraphQLCollection(GraphQLForeignKey, "files",
                          "enterprises.ContributionFile"),
        GraphQLCollection(GraphQLForeignKey, "codelanguages",
                          "enterprises.CodeLanguageStatistic"),
    ]

    def __str__(self):
        # (commit) cid
        return f"({self.type}) {self.cid}"


class ContributionFile(models.Model):
    feed = ParentalKey(
        "ContributionFeed",
        related_name="file_contribution_feed",
        on_delete=models.SET_NULL,
        null=True,
    )
    insertions = models.IntegerField(null=True)
    deletions = models.IntegerField(null=True)
    path = models.CharField(null=True, max_length=255)
    raw_changes = models.TextField(null=True, max_length=255)

    graphql_fields = [
        GraphQLForeignKey("page", content_type="enterprises.Contributor"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("path"),
        GraphQLString("raw_changes"),
    ]

    def __str__(self):
        # /src/test.py (+100/-200)
        return f"{self.path} (+{self.insertions}/-{self.deletions})"


class CodeLanguageStatistic(models.Model):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_codelanguage_statistic",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    type = models.CharField(null=True, max_length=255, default="Unkown")
    color = models.CharField(null=True, max_length=255, default="Unkown")
    primary_extension = models.CharField(null=True,
                                         max_length=255,
                                         default="Unkown")
    insertions = models.IntegerField(null=True, default=0)
    deletions = models.IntegerField(null=True, default=0)

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("type"),
        GraphQLString("color"),
        GraphQLString("primary_extension"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
    ]


class CodeTransitionStatistic(models.Model):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_codetransition_statistic",
        on_delete=models.SET_NULL,
        null=True,
    )

    insertions = models.IntegerField(null=True, default=0)
    deletions = models.IntegerField(null=True, default=0)
    datetime = models.DateTimeField(null=True)

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("datetime"),
    ]


class Contributor(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_contributors",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    username = models.CharField(null=True, max_length=255, default="Unkown")
    active = models.BooleanField(default=True)
    avatar = models.ImageField(null=True)
    contribution_feed = ParentalManyToManyField(
        "ContributionFeed", related_name="contributor_feed", blank=True)
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic",
        related_name="contributor_codelanguages",
        blank=True,
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic",
        related_name="contributor_codetransition",
        blank=True,
    )

    graphql_fields = [
        GraphQLForeignKey("page",
                          content_type="enterprises.EnterpriseFormPage"),
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLBoolean("active"),
        GraphQLImage("avatar"),
        GraphQLCollection(GraphQLForeignKey, "contribution_feed",
                          "enterprises.ContributionFeed"),
        GraphQLCollection(GraphQLForeignKey, "codelanguages",
                          "enterprises.CodeLanguageStatistic"),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "enterprises.CodeTransitionStatistic",
        ),
    ]

    def __str__(self):
        return f"{self.username}"


class ProjectContributor(ClusterableModel):
    project = ParentalKey(
        "Project",
        related_name="project_projectcontributor",
        on_delete=models.CASCADE,
        null=True,
    )
    name = models.CharField(null=True, max_length=255, default="Unkown")
    username = models.CharField(null=True, max_length=255, default="Unkown")
    active = models.BooleanField(default=True)
    avatar = models.ImageField(null=True)
    contribution_feed = ParentalManyToManyField(
        "ContributionFeed", related_name="projectcontributor_feed", blank=True)
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic",
        related_name="projectcontributor_codelanguages",
        blank=True,
    )
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic",
        related_name="projectcontributor_codetransition",
        blank=True,
    )

    graphql_fields = [
        GraphQLForeignKey("project",
                          content_type="enterprises.ProjectContributor"),
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLBoolean("active"),
        GraphQLImage("avatar"),
        GraphQLCollection(GraphQLForeignKey, "contribution_feed",
                          "enterprises.ContributionFeed"),
        GraphQLCollection(GraphQLForeignKey, "codelanguages",
                          "enterprises.CodeLanguageStatistic"),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "enterprises.CodeTransitionStatistic",
        ),
    ]

    def __str__(self):
        return f"{self.username}"


class Project(ClusterableModel):
    page = ParentalKey(
        "EnterpriseFormPage",
        related_name="enterprise_projects",
        on_delete=models.SET_NULL,
        null=True,
    )

    name = models.CharField(null=True,
                            blank=True,
                            max_length=255,
                            default="Unkown")
    url = models.URLField(null=True,
                          blank=True,
                          max_length=255,
                          default="https://example.local")
    description = models.TextField(null=True, blank=True, default="Unkown")
    owner_name = models.CharField(null=True,
                                  blank=True,
                                  max_length=255,
                                  default="Unkown")
    owner_username = models.CharField(null=True,
                                      blank=True,
                                      max_length=255,
                                      default="Unkown")
    owner_email = models.EmailField(null=True,
                                    blank=True,
                                    default="test@snek.at")
    contributors = ParentalManyToManyField("ProjectContributor",
                                           related_name="project_contributor",
                                           blank=True)
    contribution_feed = ParentalManyToManyField("ContributionFeed",
                                                related_name="project_feed",
                                                blank=True)
    codelanguages = ParentalManyToManyField(
        "CodeLanguageStatistic",
        related_name="project_codelanguages",
        blank=True)
    codetransition = ParentalManyToManyField(
        "CodeTransitionStatistic",
        related_name="project_codetransition",
        blank=True)

    graphql_fields = [
        GraphQLForeignKey("page", content_type="enterprises.Project"),
        GraphQLString("name"),
        GraphQLString("url"),
        GraphQLString("description"),
        GraphQLString("owner_name"),
        GraphQLString("owner_username"),
        GraphQLString("owner_email"),
        GraphQLCollection(GraphQLForeignKey, "contribution_feed",
                          "enterprises.ContributionFeed"),
        GraphQLCollection(GraphQLForeignKey, "contributors",
                          "enterprises.ProjectContributor"),
        GraphQLCollection(GraphQLForeignKey, "codelanguages",
                          "enterprises.CodeLanguageStatistic"),
        GraphQLCollection(
            GraphQLForeignKey,
            "codetransition",
            "enterprises.CodeTransitionStatistic",
        ),
    ]


# > Pages
class EnterpriseFormField(AbstractFormField):
    page = ParentalKey("EnterpriseFormPage",
                       on_delete=models.CASCADE,
                       related_name="form_fields")


class EnterpriseFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class EnterpriseFormPage(BaseEmailFormPage):
    # Only allow creating HomePages at the root level
    template = 'patterns/pages/enterprises/enterprise_index_page.html'

    parent_page_types = ["EnterpriseIndex"]
    subpage_types = []
    graphql_fields = []

    show_in_menus_default = False

    class Meta:
        verbose_name = "Enterprise Form Page"

    """[Tabs]
    Wagtail content and API definition of all tabs
    """
    # ContributionFeed
    graphql_fields += [
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_contribution_feed",
            "enterprises.ContributionFeed",
        ),
    ]
    # Contributors
    contributor_panel = [
        InlinePanel("enterprise_contributors", heading="Contributors")
    ]

    graphql_fields += [
        GraphQLCollection(GraphQLForeignKey, "enterprise_contributors",
                          "enterprises.Contributor")
    ]
    # Projects
    project_panel = [
        InlinePanel("enterprise_projects", heading="Contributors")
    ]

    graphql_fields += [
        GraphQLCollection(GraphQLForeignKey, "enterprise_projects",
                          "enterprises.Project"),
    ]
    # CodeLanguageStatistic
    codelangaugestatistic_panel = [
        InlinePanel("enterprise_codelanguage_statistic",
                    heading="Language Statistic")
    ]

    graphql_fields += [
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_codelanguage_statistic",
            "enterprises.CodeLanguageStatistic",
        ),
    ]
    # CodeTransitionStatistic
    codetransitionstatistic_panel = [
        InlinePanel("enterprise_codetransition_statistic",
                    heading="Language Statistic")
    ]

    graphql_fields += [
        GraphQLCollection(
            GraphQLForeignKey,
            "enterprise_codetransition_statistic",
            "enterprises.CodeTransitionStatistic",
        ),
    ]
    # Users
    user = ParentalKey("user.SNEKUser",
                       on_delete=models.CASCADE,
                       related_name="enterprisepage")

    # Imprint
    city = models.CharField(null=True, blank=True, max_length=255)
    zip_code = models.CharField(null=True, blank=True, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    telephone = models.CharField(null=True, blank=True, max_length=255)
    telefax = models.CharField(null=True, blank=True, max_length=255)
    vat_number = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_telephone = models.CharField(null=True,
                                          blank=True,
                                          max_length=255)
    whatsapp_contactline = models.CharField(null=True,
                                            blank=True,
                                            max_length=255)
    tax_id = models.CharField(null=True, blank=True, max_length=255)
    trade_register_number = models.CharField(null=True,
                                             blank=True,
                                             max_length=255)
    court_of_registry = models.CharField(null=True, blank=True, max_length=255)
    place_of_registry = models.CharField(null=True, blank=True, max_length=255)
    ownership = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    employee_count = models.CharField(null=True, blank=True, max_length=255)
    opensource_url = models.URLField(null=True, blank=True)
    recruiting_url = models.URLField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)

    imprint_panels = [
        FieldPanel('user'),
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

    graphql_fields += [
        GraphQLString("cache"),
    ]

    edit_handler = TabbedInterface([
        # ObjectList(Page.content_panels + overview_panels, heading="Overview"),
        ObjectList(Page.content_panels, heading="Overview"),
        ObjectList(codelangaugestatistic_panel, heading="Language Statistic"),
        ObjectList(codetransitionstatistic_panel,
                   heading="Transition Statistic"),
        ObjectList(contributor_panel, heading="Contributors"),
        ObjectList(project_panel, heading="Projects"),
        ObjectList(imprint_panels, heading="Imprint"),
        ObjectList(form_panels, heading="Form"),
        ObjectList(
            BasePage.promote_panels + BasePage.settings_panels + cache_panels,
            heading="Settings",
            classname="settings",
        ),
    ])

    def get_submission_class(self):
        return EnterpriseFormSubmission

    # Create a new user
    def create_enterprise_user(
        self,
        company_username,
        enterprise_imprint,
        enterprise_contributors,
        enterprise_projects,
        enterprise_codelanguage_statistic,
        enterprise_codetransition_statistic,
    ):
        # enter the data here
        #enterprise_page = get_user_model().objects.get(username=company_username)

        enterprise_page = Page.objects.get(
            slug=f"e-{company_username}").specific

        obj_enterprise_imprint = json.loads(enterprise_imprint)
        obj_enterprise_contributors = json.loads(enterprise_contributors)
        obj_enterprise_projects = json.loads(enterprise_projects)
        obj_enterprise_codelanguage_statistic = json.loads(
            enterprise_codelanguage_statistic)
        obj_enterprise_codetransition_statistic = json.loads(
            enterprise_codetransition_statistic)

        enterprise_page.update(
            city=obj_enterprise_imprint["city"],
            zip_code=obj_enterprise_imprint["zip_code"],
            address=obj_enterprise_imprint["address"],
            telephone=obj_enterprise_imprint["telephone"],
            telefax=obj_enterprise_imprint["telefax"],
            vat_number=obj_enterprise_imprint["vat_number"],
            whatsapp_telephone=obj_enterprise_imprint["whatsapp_telephone"],
            whatsapp_contactline=obj_enterprise_imprint[
                "whatsapp_contactline"],
            tax_id=obj_enterprise_imprint["tax_id"],
            trade_register_number=obj_enterprise_imprint[
                "trade_register_number"],
            court_of_registry=obj_enterprise_imprint["court_of_registry"],
            place_of_registry=obj_enterprise_imprint["place_of_registry"],
            ownership=obj_enterprise_imprint["ownership"],
            email=obj_enterprise_imprint["email"],
            employee_count=obj_enterprise_imprint["employee_count"],
            opensource_url=obj_enterprise_imprint["opensource_url"],
            recruiting_url=obj_enterprise_imprint["recruiting_url"],
            description=obj_enterprise_imprint["description"],
        )

        enterprise_page.enterprise_contributors.add(
            name=obj_enterprise_contributors["name"],
            username=obj_enterprise_contributors["username"],
            active=obj_enterprise_contributors["active"],
            avatar=obj_enterprise_contributors["avatar"],
        )

        codelanguages = json.loads(enterprise_contributors["codelanguages"]),
        codetransition = json.loads(enterprise_contributors["codetransition"]),

        enterprise_page.enterprise_projects.add(
            name=obj_enterprise_projects["name"],
            url=obj_enterprise_projects["url"],
            description=obj_enterprise_projects["description"],
            owner_name=obj_enterprise_projects["owner_name"],
            owner_username=obj_enterprise_projects["owner_username"],
            owner_email=obj_enterprise_projects["owner_email"],
        )

        contributors = json.loads(enterprise_projects["contributors"]),
        codelanguages = json.loads(enterprise_projects["codelanguages"]),
        codetransition = json.loads(enterprise_projects["codetransition"]),

        enterprise_page.enterprise_codelanguage_statistic.add(
            name=obj_enterprise_codelanguage_statistic["name"],
            type=obj_enterprise_codelanguage_statistic["type"],
            color=obj_enterprise_codelanguage_statistic["color"],
            primary_extension=obj_enterprise_codelanguage_statistic[
                "primary_extension"],
            insertions=obj_enterprise_codelanguage_statistic["insertions"],
            deletions=obj_enterprise_codelanguage_statistic["deletions"],
        )

        enterprise_page.enterprise_codelanguage_statistic.add(
            name=obj_enterprise_codelanguage_statistic["name"],
            type=obj_enterprise_codelanguage_statistic["type"],
            color=obj_enterprise_codelanguage_statistic["color"],
            primary_extension=obj_enterprise_codelanguage_statistic[
                "primary_extension"],
            insertions=obj_enterprise_codelanguage_statistic["insertions"],
            deletions=obj_enterprise_codelanguage_statistic["deletions"],
        )

        enterprise_page.code_transition_statistic.update()

        enterprise_page.save_revision().publish()

        user = enterprise_page.user

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

        user = self.create_enterprise_user(
            company_username=form.cleaned_data["company_name"],
            enterprise_imprint=form.cleaned_data["enterprise_imprint"],
            enterprise_contributors=form.
            cleaned_data["enterprise_contributors"],
            enterprise_projects=form.cleaned_data["enterprise_projects"],
            enterprise_codelanguage_statistic=form.
            cleaned_data["enterprise_codelanguage_statistic"],
            enterprise_codetransition_statistic=form.
            cleaned_data["enterprise_codetransition_statistic"],
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


class EnterpriseIndex(BasePage):
    template = 'patterns/pages/enterprises/enterprise_index_page.html'

    # Only allow creating HomePages at the root level
    parent_page_types = ["home.HomePage"]
    subpage_types = ["EnterpriseFormPage"]

    class Meta:
        verbose_name = "Enterprise Index"

    def get_context(self, request, *args, **kwargs):
        enterprises = EnterpriseFormPage.objects.live().public().descendant_of(
            self).order_by('slug')

        page_number = request.GET.get('page', 1)
        paginator = Paginator(enterprises, settings.DEFAULT_PER_PAGE)
        try:
            enterprises = paginator.page(page_number)
        except PageNotAnInteger:
            enterprises = paginator.page(1)
        except EmptyPage:
            enterprises = paginator.page(paginator.num_pages)

        context = super().get_context(request, *args, **kwargs)
        context.update(enterprises=enterprises)

        return context