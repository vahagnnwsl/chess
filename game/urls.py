from django.urls import path
from game.views import *

urlpatterns = [
    path('/room/<str:hash>', room, name='game'),
    path('/room/<str:hash>/fen', save_fen),
    path('/room/<str:hash>/checkmate', checkmate),
    path('/create_room', create_room, name='create_room'),
]
