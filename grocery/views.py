from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from grocery.forms import CreateUserForm, LoginForm
from grocery.models import ContactMessage


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

def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Make sure you're using .get(), not ()
        subject = request.POST.get('subject')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Save the data to the database
        contact_message = ContactMessage(
            email=email,
            subject=subject,
            phone_number=phone_number,
            message=message
        )
        contact_message.save()

        messages.success(request, "Message has been sent successfully!")

    return render(request, 'about-us.html')


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
