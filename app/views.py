from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ContactUs, Hostel
from .models import AboutUs
import re
from django.db.models import Q
from django.core.mail import send_mail
from GharKhoji.settings import EMAIL_HOST_USER
#user role
from django.contrib.auth import get_user_model
User = get_user_model() 

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
        role = request.POST.get('role')

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

        if not role:
            errors['role'] = "Role is required."
        if errors:
            return render(request, 'signup.html', {'errors': errors})

        my_user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password, role=role)
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
    budget = request.GET.get('budget')
    # Apply filters based on the user inputs
    if name:
        hostels = hostels.filter(Q(title__icontains=name))
    if location:
        hostels = hostels.filter(Q(location__icontains=location))
    if hostel_type:
        hostels = hostels.filter(Q(type__icontains=hostel_type))
    if budget:
        try:
            budget = int(budget)  # Convert budget to integer
            hostels = hostels.filter(single_room_price__exact=budget)  # Filter by max price
        except ValueError:
            pass  # Ignore invalid budget values 
    return render(request, 'hostel.html', {'hostels': hostels})


def HostelDetails(request, id):
    hostel = get_object_or_404(Hostel, id=id)
    return render(request, 'hosteldetails.html', {'hostel': hostel})

#Forgot Password
def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print("Email: ", email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("User Exists")
            send_mail("Reset Your Password", f"Hello User: {user}!\nTo reset password, click on the given link \n http://127.0.0.1:8000/newpassword/{user}", EMAIL_HOST_USER, [email], fail_silently=True)
            messages.success(request, "Password reset link has been sent to your email.")
        else:
            return render(request, 'forgotpassword.html', {"errors": {"email": "Email does not exist"}})
    return render(request, 'forgotpassword.html')

#New Password
def NewPasswordPage(request, username):
    userid = get_object_or_404(User, username=username)
    errors = {}
    if request.method== "POST":
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        # Password validation pattern
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        # Validate password
        if not password:
            errors['password'] = "Password is required."
        elif not re.match(password_pattern, password):
            errors['password'] = "Password must be at least 8 characters, contain one uppercase, one lowercase, one number, and one special character." 
        # Validate confirm password
        if not confirmpassword:
            errors['confirmpassword'] = "Confirm password is required."
        elif password != confirmpassword:
            errors['confirmpassword'] = "Passwords do not match."

        # If there are errors, re-render the form with errors
        if errors:
            return render(request, 'newpassword.html', {'errors': errors})      
        
        # Set new password and save user
        userid.set_password(password)
        userid.save()
        return redirect('message')
    return render(request, 'newpassword.html')

#Message 
def Message(request):
    return render(request, 'message.html')

#Booking 
def Booking(request):
    return render(request, 'bookingdetail.html')


#User Profile Section
def my_account(request):
    user = request.user

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        # Validate the data
        if not first_name or not last_name or not email or not username:
            messages.error(request, "All fields are required.")
            return redirect('profile')  # Redirect back to the same page

        # Update user model fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        try:
            # Save the updated user details to the database
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

        return redirect('my_account')  # After saving, redirect to the same page

    return render(request, 'profile.html', {'user': user})

def saved(request):
    return render(request, 'home.html')


def bookings(request):
    return render(request, 'home.html')

