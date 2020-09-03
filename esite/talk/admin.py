from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Talk

# Register your models here.


class TalkAdmin(ModelAdmin):
    model = Talk
    menu_label = "Talk"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = (
        "title",
        "description",
        "path",
        "url",
        "display_url",
        "download_url",
    )
    search_fields = (
        "title",
        "description",
        "path",
        "url",
        "display_url",
        "download_url",
    )


modeladmin_register(TalkAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
