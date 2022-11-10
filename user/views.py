from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            username = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email Or Password Is Incorrect')


    context = {

    }
    return render(request, 'user/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redierect('home')
