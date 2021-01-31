def active_game(request):
    conn = False

    if request.user:
        if request.user.id and isinstance(request.user.id, int):
            conn = True

    return {'request': conn}
