from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from game.models import Room
from account.models import User
from datetime import datetime
import hashlib
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from game.helpers import sort_moves


@require_http_methods(["POST"])
@login_required
def create_room(request):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    hash = hashlib.md5((time + request.user.username).encode())
    room = Room(user_1_id=request.user.id, hash=hash.hexdigest())
    room.save()
    return redirect('game', room.hash)


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

        moves = room.moves

        if moves:

            moves = sort_moves(json.loads(moves))

        else:
            moves = []

        if room.is_finish:
            return render(request, 'game/pages/finish_room.html', {'room': room,'opponent': opponent,})

        return render(request, 'game/pages/room.html',
                      {'room': room, 'orientation': orientation, 'opponent': opponent, 'moves': moves})
    else:
        return redirect('home')


@require_http_methods(["POST"])
@csrf_exempt
def save_fen(request, hash):
    try:

        room = Room.objects.get(hash=hash)

        move = json.loads(request.POST['move'])
        moves = room.moves

        if moves:
            moves = json.loads(moves)
        else:
            moves = []

        moves.append(move)
        room.fen = request.POST['fen']
        room.moves = json.dumps(moves)
        room.save()
        moves = sort_moves(json.loads(room.moves))
        return JsonResponse(status=200, data=moves, safe=False)
    except Room.DoesNotExist:
        return JsonResponse(status=411, data={})


@require_http_methods(["POST"])
@csrf_exempt
def checkmate(request, hash):
    try:

        room = Room.objects.get(hash=hash)
        room.is_finish = 1
        winner = User.objects.get(username=request.POST['winner'])
        room.winner_id = winner.id
        room.save()

        return JsonResponse(status=200, data={'winner': request.POST['winner']}, safe=False)
    except Room.DoesNotExist:
        return JsonResponse(status=411, data={})
