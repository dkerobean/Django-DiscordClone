from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room, Topic, Message
from .utils import searchRooms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q




# Create your views here.

def home(request):
    topics = Topic.objects.all()

    #function from utils file for search functionality
    query, room = searchRooms(request)

    room_count = room.count()
    room_messages = Message.objects.filter(
    Q(room__topic__name__icontains=query))

    context = {
        'room':room,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages
    }

    return render(request, 'home.html', context)


def showRoom(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        user_message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )
        room.participants.add(request.user)
        messages.success(request, 'Message Sent')
        return redirect('show-room', pk=room.id)


    context = {
        'room':room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

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


@login_required(login_url='login-user')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        messages.error(request, 'You do not have rights to perform this operation')
        return redirect('home')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {
        'object':message
    }
    return render(request, 'base/delete_form.html', context)
