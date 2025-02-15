from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ContactUs, Hostel
from .models import AboutUs
import re
from django.http import JsonResponse
from django.contrib.auth import authenticate

# Create your views here.
#@login_required(login_url='login')
def HomePage(request):
    hostels = Hostel.objects.all()
    return render(request, 'home.html', {'hostels':hostels})


def SignupPage(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        errors = {}

        # Validate email
        if '@gmail.com' not in email:
            errors['email'] = "Email must be a valid Gmail address."
        # Validate email uniqueness
        if User.objects.filter(email=email).exists():
            errors['email'] = "Email already exists. Please choose a different one."


        # Validate username length
        if len(username) < 4:
            errors['username'] = "Username must be at least 4 characters long."


        # Validate password complexity
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_pattern, password):
            errors['password'] = "Password must contain at least 8 characters, one uppercase, one lowercase, special cgaracter and one number."

        # Validate password match
        if password != confirmpassword:
            errors['confirmpassword'] = "Passwords do not match."

        # Validate required fields
        for field in [firstname, lastname, email, username, password, confirmpassword]:
            if not field:
                errors[field] = "This field is required."

        if errors:
            return render(request, 'signup.html', {'errors': errors})

        # Create the user if no errors
        my_user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
        my_user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')

def check_email(request):
    email = request.GET.get('email', None)
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})



def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")

        login(request, user)
        return redirect("home")  # Redirect to a homepage after successful login

    return render(request, "login.html")

from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def check_credentials(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if not username or not password:
        return JsonResponse({'status': 'error', 'message': 'Missing credentials'})

    # Check if the username exists
    if not User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'user_not_found'})

    # Authenticate user
    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'status': 'password_incorrect'})
    
    return JsonResponse({'status': 'success'})


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


from django.db.models import Q

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



