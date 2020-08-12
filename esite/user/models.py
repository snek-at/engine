import json
import uuid
import django.contrib.auth.validators
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.db import models
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

#from esite.utils.models import BasePage


# Extend AbstractUser Model from django.contrib.auth.models
class SNEKUser(AbstractUser, ClusterableModel):
    username = models.CharField(
        'username',
        null=True,
        blank=False,
        error_messages={"unique": "A user with that username already exists."},
        help_text=
        "Required. 36 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=36,
        unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
    )
    is_enterprise = models.BooleanField('enterprise',
                                        blank=False,
                                        default=False)
    sources = models.TextField(null=True, blank=False)
    cache = models.TextField(null=True, blank=False)

    # Custom save function
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())

        if not self.is_staff or self.is_enterprise:
            if not self.is_active:
                self.is_active = True

                send_mail(
                    "got activated",
                    "You got activated.",
                    "noreply@snek.at",
                    [self.email],
                    fail_silently=False,
                )

        else:
            self.is_active = False

        super(SNEKUser, self).save(*args, **kwargs)

    panels = [
        FieldPanel("username"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("email"),
        FieldPanel("is_staff"),
        FieldPanel("is_active"),
        FieldPanel("is_enterprise"),
        FieldPanel("cache"),
        InlinePanel("personpage", label="Person Page"),
        InlinePanel("enterprisepage", label="Enterprise Page"),
    ]

    graphql_fields = [
        GraphQLString("username"),
        GraphQLString("sources"),
        GraphQLString("cache"),
    ]

    def __str__(self):
        return self.username


# Extend AbstractUser Model from django.contrib.auth.models
# class UserPage(BasePage):
#     # Only allow creating HomePages at the root level
#     parent_page_types = ["wagtailcore.Page"]
#     # subpage_types = ['news.NewsIndex', 'standardpages.StandardPage', 'articles.ArticleIndex',
#     #                 'person.PersonIndex', 'events.EventIndex']

#     user_cache = models.TextField(null=True, blank=True)

#     main_content_panels = []

#     edit_handler = TabbedInterface(
#         [
#             ObjectList(
#                 BasePage.content_panels + main_content_panels, heading="Content"
#             ),
#             ObjectList(
#                 BasePage.promote_panels + BasePage.settings_panels,
#                 heading="Settings",
#                 classname="settings",
#             ),
#         ]
#     )

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
