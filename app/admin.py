from django.contrib import admin

# Register your models here.
from .models import ContactUs, Hostel, AboutUs

admin.site.register(ContactUs)
admin.site.register(AboutUs)
admin.site.register(Hostel)