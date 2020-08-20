import re

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from .widgets import ColorAlphaWidget, ColorWidget, GradientColorWidget

color_re = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
validate_color = RegexValidator(color_re, _("Enter a valid color."), "invalid")


class ColorField(forms.CharField):
    default_validators = [validate_color]
    widget = ColorWidget

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 18
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = self.ColorWidget
        return super(ColorField, self).formfield(**kwargs)

    def prepare_value(self, value):
        if isinstance(value, str):
            return value
        # or should it be
        return self.prepare_value(str(value))


class ColorAlphaField(forms.CharField):
    widget = ColorAlphaWidget

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 18
        super(ColorAlphaField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = self.ColorWidget2
        return super(ColorAlphaField, self).formfield(**kwargs)

    def prepare_value(self, value):
        if isinstance(value, str):
            return value
        # or should it be
        return self.prepare_value(str(value))


class GradientColorField(forms.CharField):
    widget = GradientColorWidget

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 100
        super(GradientColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = self.GradientColorWidget
        return super(GradientColorField, self).formfield(**kwargs)

    def prepare_value(self, value):
        if isinstance(value, str):
            return value
        # or should it be
        return self.prepare_value(str(value))


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
