from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Achievement

# Register your models here.


class AchievementAdmin(ModelAdmin):
    model = Achievement
    menu_label = "Achievement"
    menu_icon = "fa-trophy"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = (
        "collectors",
        "title",
        "description",
        "image",
        "points",
    )
    search_fields = (
        "collectors",
        "title",
        "description",
    )


modeladmin_register(AchievementAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
