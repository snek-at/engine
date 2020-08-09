from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Profile

# Register your registration related models here.


class ProfileAdmin(ModelAdmin):
    model = Profile
    menu_label = "Profile"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = (
        "date_joined",
        "first_name",
        "last_name",
    )
    search_fields = (
        "date_joined",
        "first_name",
        "last_name",
    )


#modeladmin_register(ProfileAdmin)
