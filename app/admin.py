from django.contrib import admin
from .models import ContactUs, AboutUs
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import HostelProperty, HostelImage, RegisterCertificate

class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'username', 'role', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )


class HostelImageInline(admin.TabularInline):
    """Allows adding multiple images inline in the admin panel."""
    model = HostelImage
    extra = 2  # Show 2 empty slots for adding images

class HostelCertificateInline(admin.StackedInline):
    """Allows adding one registration certificate inline in the admin panel."""
    model = RegisterCertificate
    extra = 0  # Do not allow adding more than one certificate
    max_num = 1  # Ensure only one certificate per hostel

class HostelPropertyAdmin(admin.ModelAdmin):
    list_display = (
        'unique_id', 'title', 'get_hostel_type_display', 'location', 'approval_status_symbol', 'approval_status'
    )
    list_editable = ('approval_status',)  # Allows editing approval status directly in the list view
    list_filter = ('approval_status', 'hostel_type', 'availability', 'location')
    search_fields = ('title', 'location', 'unique_id', 'phone_number', 'email', 'get_hostel_type_display')
    readonly_fields = ('unique_id', 'created_at')
    inlines = [HostelImageInline, HostelCertificateInline]  # Add inline images in admin panel

    def get_hostel_type_display(self, obj):
        """Display human-readable hostel type."""
        return obj.get_hostel_type_display()

    get_hostel_type_display.short_description = "Hostel Type"

    def approval_status_symbol(self, obj):
        """Display the approval status with symbols."""
        if obj.approval_status == 'approved':
            return format_html('<span style="color: green;">✅ Approved</span>')
        elif obj.approval_status == 'pending':
            return format_html('<span style="color: orange;">⏳ Pending</span>')
        elif obj.approval_status == 'rejected':
            return format_html('<span style="color: red;">❌ Rejected</span>')
        return obj.approval_status

    approval_status_symbol.short_description = "Approval Status Symbol"

    def display_images(self, obj):
        """Display multiple hostel images in the admin panel."""
        images = HostelImage.objects.filter(hostel=obj)
        if images.exists():
            image_html = "".join([
                f'<img src="{img.image.url}" width="50" height="50" style="border-radius: 5px; margin: 2px;" />'
                for img in images[:5]  # Limit display to 5 images
            ])
            return format_html(image_html)
        return "No Images"
    
    display_images.short_description = "Hostel Images"

    def display_amenities(self, obj):
        """Show amenities as plain text."""
        if obj.amenities:
            return obj.amenities.replace(",", ", ")  # Show amenities as comma-separated text
        return "No Amenities"

    display_amenities.short_description = "Amenities"

# Register the HostelProperty model with the customized admin view
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactUs)
admin.site.register(AboutUs)
admin.site.register(HostelProperty, HostelPropertyAdmin)
