from django.db.models import Q
from .models import Room


def searchRooms(request):
    query = ''
    if request.GET.get('q'):
        query = request.GET.get('q')

    room = Room.objects.filter(
    Q(topic__name__icontains= query) |
    Q(name__icontains= query) |
    Q(description__icontains= query)
    )

    return query, room
