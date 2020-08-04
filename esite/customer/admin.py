from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Customer


class CustomerAdmin(ModelAdmin):
    model = Customer
    menu_label = "Customer"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the customer overview
    list_display = ("date_joined", "username", "email")
    search_fields = ("date_joined", "username", "email")


# modeladmin_register(CustomerAdmin)
