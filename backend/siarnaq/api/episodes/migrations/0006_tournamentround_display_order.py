# Generated by Django 4.1.2 on 2023-01-25 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "episodes",
            "0005_remove_tournamentround_round-unique-tournament-challonge_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="tournamentround",
            name="display_order",
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]