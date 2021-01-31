from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from game.models import Room
from datetime import datetime
import hashlib
from django.http import JsonResponse


@require_http_methods(["POST"])
@login_required
def create_room(request):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    hash = hashlib.md5((time + request.user.username).encode())
    room = Room(user_1_id=request.user.id, hash=hash.hexdigest())
    room.save()
    return redirect('room', room.hash)


@require_http_methods(["GET"])
@login_required
def room(request, hash):

    try:
        room = Room.objects.get(hash=hash)
    except Room.DoesNotExist:
        return redirect('home')

    user_2_id = 0

    orientation = 'black'

    if room.user_1_id == request.user.id:
        access = True
        orientation = 'white'
    elif room.user_2_id == request.user.id:
        access = True

    elif room.user_1_id != request.user.id and not room.user_2_id:
        access = True
        user_2_id = request.user.id
    else:
        access = False

    if access:
        if user_2_id:
            room.user_2_id = user_2_id
            room.save()

        if room.user_1_id == request.user.id:
            opponent = room.user_2
        else:
            opponent = room.user_1

        return render(request, 'game/pages/room.html',
                      {'room': room, 'orientation': orientation, 'opponent': opponent})
    else:
        return redirect('home')


@require_http_methods(["POST"])
@login_required
def save_fen(request, hash):
    try:
        room = Room.objects.get(hash=hash)
        room.fen = request.POST['fen']
        room.save()
        return JsonResponse(status=200, data={})
    except Room.DoesNotExist:
        return JsonResponse(status=411, data={})
