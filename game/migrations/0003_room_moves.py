# Generated by Django 3.1.4 on 2021-02-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_room_pgn'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='moves',
            field=models.TextField(null=True),
        ),
    ]
