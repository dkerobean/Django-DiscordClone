from django.shortcuts import render, redirect
from .forms import RoomForm
from .models import Room, Topic, Message, User
from .utils import searchRooms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q




# Create your views here.

def home(request):
    topics = Topic.objects.all()[0:6]

    #function from utils file for search functionality
    query, room = searchRooms(request)

    room_count = room.count()
    topic_count = topics.count()
    room_messages = Message.objects.filter(
    Q(room__topic__name__icontains=query))

    context = {
        'room':room,
        'topics':topics,
        'room_count':room_count,
        'room_messages':room_messages,
        'topic_count':topic_count
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
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')

        )
        messages.success(request, 'Room Created Successfully')
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit = False)
        #     roo.host = request.user
        #     room.save()


    context = {
        'form':form,
        'topics':topics
    }

    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-user')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    form_name = 'update'

    if request.user != room.host:
        messages.error(request, 'You do not have rights to perform this operation')
        return redirect('home')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        messages.success(request, 'Room Updated')
        return redirect('home')

        # form = room = RoomForm(request.POST, instance = room)
        # if form.is_valid():
        #     form.save()


    context = {
        'form':form,
        'topics':topics,
        'room':room,
        'form_name':form_name
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



def mobileTopics(request):
    q = ''
    if request.GET.get('q'):
        q = request.GET.get('q')

    topics = Topic.objects.filter(name__icontains=q)

    context = {
    'topics':topics
    }

    return render(request, 'base/topics.html',context)

def showActivity(request):

    room_messages = Message.objects.all()

    context = {
    'room_messages':room_messages
    }
    return render(request, 'base/activity.html', context)
