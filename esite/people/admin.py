from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Person

# Register your registration related models here.


class PersonAdmin(ModelAdmin):
    model = Person
    menu_label = "Person"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    # list_display = ("username",)
    # search_fields = ("username",)


# modeladmin_register(PersonAdmin)
