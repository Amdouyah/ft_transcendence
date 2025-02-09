# Generated by Django 3.2.7 on 2024-10-24 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0002_tournamentplayer_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournamentgame',
            name='game',
        ),
        migrations.RemoveField(
            model_name='tournamentgame',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='tournamentgame',
            name='player2',
        ),
        migrations.RemoveField(
            model_name='tournamentgame',
            name='tournament',
        ),
        migrations.AlterUniqueTogether(
            name='tournamentplayer',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='tournamentplayer',
            name='player',
        ),
        migrations.RemoveField(
            model_name='tournamentplayer',
            name='tournament',
        ),
        migrations.DeleteModel(
            name='Tournament',
        ),
        migrations.DeleteModel(
            name='TournamentGame',
        ),
        migrations.DeleteModel(
            name='TournamentPlayer',
        ),
    ]
