from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('hostel_owner', 'Hostel Owner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


    def save(self, *args, **kwargs):
        # Automatically set role to "Admin" if the user is a superuser
        if self.is_superuser:
            self.role = "Admin"
        super().save(*args, **kwargs)
        
# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(validators=[validate_email])
    subject = models.CharField(max_length=255)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True) 
    replied = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return f"Inquiry from {self.name}"


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='hostel_images/')

    class Meta:
        verbose_name_plural = "About Us"

    def __str__(self):
        return self.title 
    

import random
from django.core.validators import FileExtensionValidator
class HostelProperty(models.Model):
    HOSTEL_TYPES = [
        ('Boy', 'Boy'),
        ('Girl', 'Girl')
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    AVAILABILITY_STATUS = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable')
    ]
    unique_id = models.CharField(max_length=10, unique=True, editable=False)
    title = models.CharField(max_length=255)
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPES)
    description = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=255)
    # Map Location Fields
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    single_beds = models.PositiveIntegerField()
    shared_2_beds = models.PositiveIntegerField()
    shared_3_beds = models.PositiveIntegerField()
    price_single_bed = models.DecimalField(max_digits=10, decimal_places=2)
    price_shared_2_beds = models.DecimalField(max_digits=10, decimal_places=2)
    price_shared_3_beds = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=15, choices=AVAILABILITY_STATUS)
    rules = models.TextField()
    pan_number = models.CharField(max_length=50)
    amenities = models.TextField()  # Store as JSON or comma-separated values
    approval_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
  
  

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = str(random.randint(1000, 9999))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Hostel Details"
    def __str__(self):
        return self.title
   
class HostelImage(models.Model):
    hostel = models.ForeignKey(HostelProperty, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_images/')
    
    def __str__(self):
        return f"Image for {self.hostel.title}"

class RegisterCertificate(models.Model):
    hostel = models.OneToOneField(HostelProperty, on_delete=models.CASCADE, related_name='certificate')
    certificate = models.FileField(
        upload_to='certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return f"Register certificate of {self.hostel.title}"
