# Generated by Django 4.1.2 on 2023-01-23 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("compete", "0005_rename_challonge_id_match_external_id_private_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="matchparticipant",
            old_name="external_id",
            new_name="external_id_private",
        ),
        migrations.AddField(
            model_name="match",
            name="external_id_public",
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="matchparticipant",
            name="external_id_public",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]