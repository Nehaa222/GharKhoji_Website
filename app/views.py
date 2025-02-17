from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ContactUs, Hostel
from .models import AboutUs
import re
from django.db.models import Q
from django.contrib.auth import authenticate

# Create your views here.
#@login_required(login_url='login')
def HomePage(request):
    hostels = Hostel.objects.all()
    return render(request, 'home.html', {'hostels':hostels})

#SIGNUP LOGIC
def SignupPage(request):
    errors = {}
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if not firstname:
            errors['firstname'] = "First Name is required."
        if not lastname:
            errors['lastname'] = "Last Name is required."
        if not email:
            errors['email'] = "Email is required."
        elif '@gmail.com' not in email:
            errors['email'] = "Email must be a valid Gmail address."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists. Please choose a different one."

        if not username:
            errors['username'] = "Username is required."
        elif len(username) < 4:
            errors['username'] = "Username must be at least 4 characters long."

        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not password:
            errors['password'] = "Password is required."
        elif not re.match(password_pattern, password):
            errors['password'] = "Password must contain atleast 8 characters, one uppercase, lowercase, number, and special character."

        if not confirmpassword:
            errors['confirmpassword'] = "Confirm password is required."
        elif password != confirmpassword:
            errors['confirmpassword'] = "Passwords do not match."

        if errors:
            return render(request, 'signup.html', {'errors': errors})

        my_user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html', {'errors': {}})

#LOGIN LOGIC
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirect logged-in users away from the login page

    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            errors["username"] = "Username is required."
        if not password:
            errors["password"] = "Password is required."

        if not errors:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")
            else:
                # Check if username exists in the database
                if not User.objects.filter(username=username).exists():
                    errors["username"] = "Username does not exist."
                else:
                    errors["password"] = "Incorrect password."

        return render(request, "login.html", {"errors": errors, "username": username})

    return render(request, "login.html", {"errors": {}})

#LOGOUT LOGIC
def LogoutPage(request):
    logout(request)
    return redirect('login')

#ABOUTUS PAGE LOGIC
def AboutPage(request):
    about_content = AboutUs.objects.first()  # Fetch the first record
    return render(request, 'aboutus.html', {'about_content': about_content})

#CONTACTPAGE LOGIC
def ContactPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Basic validation
        if not name or not phone or not subject or not message:
            messages.error(request, "All fields are required!")
            return redirect('contactus')
        
        # Phone number validation (must contain exactly 10 digits)
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Number must contain exactly 10 digits!")
            return redirect('contactus')
        
        # Save inquiry to the database
        contactus = ContactUs(name=name, phone=phone, subject=subject, message=message)
        contactus.save()
        messages.success(request, "Inquirey Sent Successfully")
        return redirect('contactus')
    
    return render(request, 'contactus.html')



def HostelPage(request):
    hostels = Hostel.objects.all()  # Fetch all hostels initially
    
    # Get the search filters from the GET request
    name = request.GET.get('title')
    location = request.GET.get('location')
    hostel_type = request.GET.get('type')
    
    # Apply filters based on the user inputs
    if name:
        hostels = hostels.filter(Q(title__icontains=name))
    if location:
        hostels = hostels.filter(Q(location__icontains=location))
    if hostel_type:
        hostels = hostels.filter(Q(type__icontains=hostel_type))
    
    return render(request, 'hostel.html', {'hostels': hostels})



def HostelDetails(request, id):
    hostel = get_object_or_404(Hostel, id=id)
    return render(request, 'hosteldetails.html', {'hostel': hostel})



