from django.db import models
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
    subject = models.CharField(max_length=255)
    message = models.TextField()
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
    

