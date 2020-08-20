import re

from django import forms
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _


class ColorWidget(forms.Widget):
    template_name = "colorfield/color.html"

    def __init__(self, attrs=None):
        self.attrs = attrs
        super(ColorWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None, **_kwargs):
        return render_to_string("colorfield/color.html", locals())

    def render_block(self, prefix, field_value, attrs={}, renderer=None, **_kwargs):
        attrs.update(self.attrs)
        value = field_value
        name = prefix
        is_required = self.is_required
        rendered = super(ColorWidget, self).render(
            name, value, attrs={}, renderer=None, **_kwargs
        )
        return render_to_string("colorfield/color.html", locals())

    def value_from_datadict(self, data, files, name):
        ret = super(ColorWidget, self).value_from_datadict(data, files, name)
        # Add a hash mark if needed so browser reads value as hex code for color
        if ret.startswith("#"):
            return ret
        ret = "#%s" % ret if ret else ret
        return ret

    class Media:
        if settings.DEBUG:
            js = ["colorfield/jscolor/jscolor.js"]
        else:
            js = ["colorfield/jscolor/jscolor.min.js"]


class ColorAlphaWidget(forms.Widget):
    template_name = "colorfield2/color.html"

    def __init__(self, attrs=None):
        self.attrs = attrs
        super(ColorAlphaWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None, **_kwargs):
        return render_to_string("colorfield2/color.html", locals())

    def render_block(self, prefix, field_value, attrs={}, renderer=None, **_kwargs):
        attrs.update(self.attrs)
        value = field_value
        name = prefix
        is_required = self.is_required
        rendered = super(ColorAlphaWidget, self).render(
            name, value, attrs={}, renderer=None, **_kwargs
        )
        return render_to_string("colorfield2/color.html", locals())

    def value_from_datadict(self, data, files, name):
        ret = super(ColorAlphaWidget, self).value_from_datadict(data, files, name)
        # Add a hash mark if needed so browser reads value as hex code for color
        if ret.startswith("#"):
            return ret
        ret = "#%s" % ret if ret else ret
        return ret

    class Media:
        if settings.DEBUG:
            js = ["colorfield2/js/colors.js", "colorfield2/js/jqColorPicker.js"]
        else:
            js = ["colorfield2/js/colors.js", "colorfield2/js/jqColorPicker.js"]


class GradientColorWidget(forms.Widget):
    template_name = "gradient_colorfield/gradient_color.html"

    def __init__(self, attrs=None):
        self.attrs = attrs
        super(GradientColorWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None, **_kwargs):
        is_required = self.is_required
        return render_to_string("gradient_colorfield/gradient_color.html", locals())

    def render_block(self, prefix, field_value, attrs={}, renderer=None, **_kwargs):
        attrs.update(self.attrs)
        value = field_value
        name = prefix
        is_required = self.is_required
        rendered = super(GradientColorWidget, self).render(
            name, value, attrs={}, renderer=None, **_kwargs
        )
        return render_to_string("gradient_colorfield/gradient_color.html", locals())

    def value_from_datadict(self, data, files, name):
        ret = super(GradientColorWidget, self).value_from_datadict(data, files, name)
        ret = "{}".format(ret) if ret else ret
        return ret

    class Media:
        js = ("gradient_colorfield/lgcolor/lgcolor.js",)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
