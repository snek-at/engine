from django.contrib.auth import get_user_model

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from esite.enterprises.admin import EnterpriseAdmin
from esite.people.admin import PersonAdmin
from esite.profile.admin import ProfileAdmin
from esite.registration.admin import RegistrationAdmin

# Register your user related models here.


class UserAdmin(ModelAdmin):
    model = get_user_model()
    menu_label = "Person"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the user overview
    list_display = ("date_joined", "username", "email")
    search_fields = ("date_joined", "username", "email")


class UserManagementAdmin(ModelAdminGroup):
    menu_label = "User Management"
    menu_icon = "group"
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (ProfileAdmin, PersonAdmin, EnterpriseAdmin, RegistrationAdmin)


modeladmin_register(UserManagementAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
