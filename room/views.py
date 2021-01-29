from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from room.models import Room
from datetime import datetime
import hashlib
from django.http import JsonResponse


@require_http_methods(["POST"])
@login_required
def create_room(request):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    hash = hashlib.md5((time + request.user.username).encode())
    room = Room(player_1_id=request.user.id, hash=hash.hexdigest())
    room.save()
    return redirect('room', room.hash)


@require_http_methods(["GET"])
@login_required
def room(request, hash):
    try:
        room = Room.objects.get(hash=hash)
    except Room.DoesNotExist:
        return redirect('home')

    player_2_id = 0

    orientation = 'black'

    if room.player_1_id == request.user.id:
        access = True
        orientation = 'white'
    elif room.player_2_id == request.user.id:
        access = True

    elif room.player_1_id != request.user.id and not room.player_2_id:
        access = True
        player_2_id = request.user.id
    else:
        access = False

    if access:
        if player_2_id:
            room.player_2_id = player_2_id
            room.save()
        return render(request, 'room/pages/room.html', {'request': request, 'room': room, 'orientation': orientation})
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
