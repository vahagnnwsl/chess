# Generated by Django 3.1.4 on 2021-02-02 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20210202_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='winner_id',
            new_name='winner',
        ),
    ]