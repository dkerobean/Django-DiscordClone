from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from base.models import Topic, Message


# Create your views here.

def loginUser(request):
    page = 'login'

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
        'page':page
    }
    return render(request, 'user/login_register.html', context)


def registerUser(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Registration successfull')
            return redirect('home')
        else:
            messages.error(request, 'An error occured please try  again')

    context = {
        'form':form
    }

    return render(request, 'user/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redierect('home')


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()

    context = {
        'user':user,
        'room':room,
        'topics':topics,
        'room_messages':room_messages

    }
    return render(request, 'user/profile.html', context)
