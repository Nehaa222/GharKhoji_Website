from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method=='POST':
      uname=request.POST.get('username')
      email=request.POST.get('email')
      password=request.POST.get('password')
      cpassword=request.POST.get('confirmpasssword')
      my_user=User.objects.create_user(uname,email,password)
      my_user.save()
      return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("User not found.")
    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def AboutPage(request):
    return render(request, 'aboutus.html')

def ContactPage(request):
    return render(request, 'contactus.html')
