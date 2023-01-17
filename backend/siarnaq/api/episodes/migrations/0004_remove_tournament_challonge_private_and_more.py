# Generated by Django 4.1.2 on 2023-01-17 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("episodes", "0003_tournament_challonge_id_private_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tournament",
            name="challonge_private",
        ),
        migrations.RemoveField(
            model_name="tournament",
            name="challonge_public",
        ),
        migrations.RemoveField(
            model_name="tournament",
            name="in_progress",
        ),
        migrations.AddField(
            model_name="tournamentround",
            name="in_progress",
            field=models.BooleanField(default=False),
        ),
    ]