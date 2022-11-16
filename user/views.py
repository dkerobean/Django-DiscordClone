from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from base.models import Topic, Message
from django.contrib.auth.decorators import login_required
from .forms import UserForm


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
    return redirect('home')


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    topic_count = Topic.objects.all().count()

    context = {
        'user':user,
        'room':room,
        'topics':topics,
        'topic_count':topic_count,
        'room_messages':room_messages

    }
    return render(request, 'user/profile.html', context)

@login_required(login_url='login-user')
def updateUser(request):
    user = request.user

    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {
    'form':form
    }

    return render(request, 'user/update_user.html',context)
