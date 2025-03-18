"""
URL configuration for GharKhoji project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #password reset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hostels/', views.hostel_locations, name='hostel_locations'),  # API for map markers
    path('signup/',views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name="logout"),
    
    path('', views.HomePage, name='home'),
    path('aboutus/', views.AboutPage, name='aboutus'),
    path('contactus/', views.ContactPage, name='contactus'),
    path('hostels/', views.HostelPage, name='hostels'),
    path('booking/', views.Booking, name='booking'),
    path('hosteldetails/<int:id>/', views.HostelDetails, name='hosteldetails'),
    
    path('forgotpassword/', views.ForgotPassword, name='forgotpassword'),
    path('newpassword/<str:username>/', views.NewPasswordPage, name='newpassword'),
    path('message/', views.Message, name='message'),
    
    path('my-account/', views.my_account, name='my_account'),
    path('saved/', views.saved, name='saved'),
    path('bookings/', views.bookings, name='bookings'),

    path('hostelownerdashboard/', views.Hostelownerdashboard, name='hostelownerdashboard'),
    path('hostelowneruser/', views.Hostelowneruser, name='hostelowneruser'),
###### Added
    path('hosteladd/', views.HostelAdd, name='hosteladd'),
    path('hostelownerprofile/', views.Hostelownerprofile, name='hostelownerprofile')
]


urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)