from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def registersUser(request):
    form = CreateUserForm()

    if request.method == "POST":
        form_data = CreateUserForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            user = form_data.cleaned_data.get("username")
            messages.success(request, "Account Created "+ user)
            return redirect("login")

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def loginUser(request):
    return render(request, 'users/login.html')