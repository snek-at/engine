from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import RedemptionCode

# Register your registration related models here.


class RedemptionAdmin(ModelAdmin):
    model = RedemptionCode
    menu_label = "Redemption"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = ("is_active", "hkey", "bid", "tid")
    search_fields = ("is_active", "hkey", "bid", "tid")


class RedemptionManagementAdmin(ModelAdminGroup):
    menu_label = "SN Management"
    menu_icon = "group"
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (RedemptionAdmin,)


modeladmin_register(RedemptionManagementAdmin)