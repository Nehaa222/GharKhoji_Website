from django.contrib import admin
from .models import ContactUs, Hostel, AboutUs
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'role', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactUs)
admin.site.register(AboutUs)
admin.site.register(Hostel)