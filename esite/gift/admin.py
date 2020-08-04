from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Register your registration related models here.

from .models import GiftCode


class GiftAdmin(ModelAdmin):
    model = GiftCode
    menu_label = "Gift"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = ("is_active", "hkey", "bid", "tid")
    search_fields = ("is_active", "hkey", "bid", "tid")


modeladmin_register(GiftAdmin)
