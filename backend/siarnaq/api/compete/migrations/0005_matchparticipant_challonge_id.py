# Generated by Django 4.1.2 on 2023-01-15 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compete", "0004_match_challonge_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="matchparticipant",
            name="challonge_id",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]