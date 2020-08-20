from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string

from wagtail.core.blocks import FieldBlock

from .forms import ColorAlphaField, ColorField, GradientColorField
from .widgets import ColorAlphaWidget, ColorWidget, GradientColorWidget


class ColorBlock(FieldBlock):
    def __init__(self, help_text=None, **kwargs):
        # 'label' and 'initial' parameters are not exposed, as Block handles that functionality natively
        # (via 'label' and 'default')
        self.field = ColorField(help_text=help_text, widget=ColorWidget)
        super().__init__(**kwargs)

    def render_form(self, value, prefix="", errors=None):
        field = self.field
        widget = field.widget

        widget_attrs = {"id": prefix, "placeholder": self.label}

        field_value = field.prepare_value(self.value_for_form(value))

        if hasattr(widget, "render_with_errors"):
            widget_html = widget.render_with_errors(
                prefix, field_value, attrs=widget_attrs, errors=errors
            )
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render_block(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string(
            "wagtailadmin/block_forms/field.html",
            {
                "name": self.name,
                "classes": self.meta.classname,
                "widget": widget_html,
                "field": field,
                "errors": errors if (not widget_has_rendered_errors) else None,
            },
        )

    class Meta:
        default = "#FFFFFF"


class ColorAlphaBlock(FieldBlock):
    def __init__(self, help_text=None, **kwargs):
        # 'label' and 'initial' parameters are not exposed, as Block handles that functionality natively
        # (via 'label' and 'default')
        self.field = ColorAlphaField(help_text=help_text, widget=ColorAlphaWidget)
        super().__init__(**kwargs)

    def render_form(self, value, prefix="", errors=None):
        field = self.field
        widget = field.widget

        widget_attrs = {"id": prefix, "placeholder": self.label}

        field_value = field.prepare_value(self.value_for_form(value))

        if hasattr(widget, "render_with_errors"):
            widget_html = widget.render_with_errors(
                prefix, field_value, attrs=widget_attrs, errors=errors
            )
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render_block(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string(
            "wagtailadmin/block_forms/field.html",
            {
                "name": self.name,
                "classes": self.meta.classname,
                "widget": widget_html,
                "field": field,
                "errors": errors if (not widget_has_rendered_errors) else None,
            },
        )

    class Meta:
        default = ""


class GradientColorBlock(FieldBlock):
    def __init__(self, help_text=None, **kwargs):
        # 'label' and 'initial' parameters are not exposed, as Block handles that functionality natively
        # (via 'label' and 'default')
        self.field = GradientColorField(help_text=help_text, widget=GradientColorWidget)
        super().__init__(**kwargs)

    def render_form(self, value, prefix="", errors=None):
        field = self.field
        widget = field.widget

        widget_attrs = {"id": prefix, "placeholder": self.label}

        field_value = field.prepare_value(self.value_for_form(value))

        if hasattr(widget, "render_with_errors"):
            widget_html = widget.render_with_errors(
                prefix, field_value, attrs=widget_attrs, errors=errors
            )
            widget_has_rendered_errors = True
        else:
            widget_html = widget.render_block(prefix, field_value, attrs=widget_attrs)
            widget_has_rendered_errors = False

        return render_to_string(
            "wagtailadmin/block_forms/field.html",
            {
                "name": self.name,
                "classes": self.meta.classname,
                "widget": widget_html,
                "field": field,
                "errors": errors if (not widget_has_rendered_errors) else None,
            },
        )

    class Meta:
        default = ""


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
