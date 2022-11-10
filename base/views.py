from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room, Topic
from .utils import searchRooms
from django.contrib.auth.decorators import login_required
from django.contrib import messages




# Create your views here.

def home(request):
    topics = Topic.objects.all()

    #function from utils file for search functionality
    query, room = searchRooms(request)

    room_count = room.count()

    context = {
        'room':room,
        'topics':topics,
        'room_count':room_count
    }
    return render(request, 'home.html', context)

@login_required(login_url='login-user')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-user')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.user != room.host:
        messages.error(request, 'You do not have rights to perform this operation')
        return redirect('home')

    if request.method == 'POST':
        form = room = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-user')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        messages.error(request, 'You do not have rights to perform this operation')
        return redirect('home')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'object':room
    }
    return render(request, 'base/delete_form.html', context)
