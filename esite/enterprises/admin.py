from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Enterprise


class EnterpriseAdmin(ModelAdmin):
    model = Enterprise
    menu_label = "Enterprise"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the enterprise overview
    list_display = ("username", )
    search_fields = ("username", )


# modeladmin_register(EnterpriseAdmin)
