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

from esite.utils.models import BasePage

# Extend AbstractUser Model from django.contrib.auth.models
class User(AbstractUser):
    username = models.CharField(
        null=True,
        blank=False,
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 36 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=36,
        unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        verbose_name="username",
    )
    is_customer = models.BooleanField(blank=False, default=False)
    registration_data = models.TextField(null=True, blank=False)

    # Custom save function
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(uuid.uuid4())

        if not self.registration_data or self.is_customer:
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

        super(User, self).save(*args, **kwargs)

    panels = [
        FieldPanel("username"),
        FieldPanel("is_customer"),
        FieldPanel("registration_data"),
    ]

    def __str__(self):
        return self.username


# Extend AbstractUser Model from django.contrib.auth.models
class UserPage(BasePage):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    # subpage_types = ['news.NewsIndex', 'standardpages.StandardPage', 'articles.ArticleIndex',
    #                 'people.PersonIndex', 'events.EventIndex']

    main_content_panels = []

    edit_handler = TabbedInterface(
        [
            ObjectList(BasePage.content_panels + main_content_panels, heading="Content"),
            ObjectList(
                BasePage.promote_panels + BasePage.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
