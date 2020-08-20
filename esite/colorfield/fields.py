import re

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .widgets import ColorAlphaWidget, ColorWidget

color_re = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
validate_color = RegexValidator(color_re, _("Enter a valid color."), "invalid")


class ColorField(models.CharField):
    default_validators = [validate_color]
    widget = ColorWidget

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 18
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


class ColorAlphaField(models.CharField):
    default_validators = [validate_color]
    widget = ColorAlphaWidget

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 18
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
