from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room


# Create your views here.

def home(request):
    room = Room.objects.all()
    context = {
        'room':room
    }
    return render(request, 'home.html', context)


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


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if request.method == 'POST':
        form = room = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'object':room
    }
    return render(request, 'base/delete_form.html', context)
