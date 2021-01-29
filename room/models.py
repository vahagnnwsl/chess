from django.db import models
from player.models import Player


class Room(models.Model):
    hash = models.CharField(max_length=100, unique=True)
    player_1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='player_1_room_set'
    )
    player_2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        null=True,
        related_name='player_2_room_set'

    )
    is_finish = models.SmallIntegerField(default=0)
    fen = models.TextField(null=True)
    win = models.CharField(max_length=255, null=True)
