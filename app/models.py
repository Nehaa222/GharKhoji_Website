from django.db import models

    
# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"


class Hostel(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    # Multiple image fields
    image1 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)

    email = models.EmailField(max_length=255, unique=True) 
    phone_number = models.CharField(max_length=15)
    description = models.TextField()
    rules = models.TextField(help_text="Enter rules separated by a newline.", blank=True)  # Store multiple rules in one field
    # Room details
    single_room_price = models.PositiveIntegerField(default=0)
    two_sharing_price = models.PositiveIntegerField(default=0)
    three_sharing_price = models.PositiveIntegerField(default=0)
    
    single_room_available = models.PositiveIntegerField(default=0)
    two_sharing_available = models.PositiveIntegerField(default=0)
    three_sharing_available = models.PositiveIntegerField(default=0)

    facilities = models.TextField(blank=True)


    def __str__(self):
        return self.title
   
class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='hostel_images/')

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title 