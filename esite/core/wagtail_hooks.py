from django.templatetags.static import static
from django.utils.html import format_html

from wagtail.core import hooks


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    # Add /static/css/custom.css to admin.
    return format_html('<link rel="stylesheet" href="{}">', static("core/custom.css"))


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    # Add /static/css/custom.css to admin.
    return format_html('<script src="{}"></script>', static("core/custom.js"))


# @hooks.register("insert_editor_js", order=100)
# def global_admin_js():
#    # Add /static/css/custom.css to admin.
#    return format_html('<script src="{}"></script>', static("wagtailadmin/page-editor.js"))

# @hooks.register('construct_main_menu')
# def hide_snippets_menu_item(request, menu_items):
#    menu_items[:] = [item for item in menu_items if item.name != 'reports']

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019 Werbeagentur Christian Aichner
