from django.http import HttpResponse
from django.db import models
from django.core.validators import RegexValidator
from wagtail.admin.edit_handlers import FieldPanel

from esite.bifrost.models import (
    GraphQLField,
    GraphQLString,
    GraphQLStreamfield,
)

# Create your homepage related models here.


class RedemptionCode(models.Model):
    hkey = models.CharField(primary_key=True, max_length=14)
    bid = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        validators=[
            RegexValidator(
                regex="^[a-f0-9]{32}$",
                message="It has to be a md5 hash",
                code="nomatch",
            )
        ],
    )
    tid = models.CharField(
        null=True,
        blank=True,
        max_length=32,
        validators=[
            RegexValidator(
                regex="^[a-f0-9]{32}$",
                message="It has to be a md5 hash",
                code="nomatch",
            )
        ],
    )
    is_active = models.BooleanField(null=False, blank=False, default=True)

    # panels = [FieldPanel("hkey"), FieldPanel("bid"), FieldPanel("tid")]

    def __str__(self):
        return self.hkey
