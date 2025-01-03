from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from grocery.forms import CreateUserForm, LoginForm


# Create your views here.
def home(request):

    return render(request, 'index.html')

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'register.html', context=context)

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'form': form}
    return render(request, 'my-login.html', context=context)

@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'dashboard.html')

def about_us(request):
    return render(request, 'about-us.html')

def user_logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("my-login")
