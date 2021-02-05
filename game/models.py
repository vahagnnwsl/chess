from django.db import models
from account.models import User


class Room(models.Model):
    hash = models.CharField(max_length=100, unique=True)
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_1_room_set'
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_2_room_set'

    )
    is_finish = models.SmallIntegerField(default=0)
    fen = models.TextField(null=True)
    pgn = models.TextField(null=True)
    moves = models.TextField(null=True)
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='winner_id_room_set'

    )
