# An API-esque module for our usage.
# Commands here are not very generic (like a good API),
# and are instead tailored to Battlecode's specific usage,
# to improve dev efficiency

import json
import os

import requests

_headers = {
    "Accept": "application/json",
    "Authorization-Type": "v1",
    # TODO refactor this into normal settings var etc
    "Authorization": os.getenv("CHALLONGE_API_KEY"),
    "Content-Type": "application/vnd.api+json",
    # requests' default user agent causes Challonge's API to crash.
    "User-Agent": "",
}

AUTH_TYPE = "v1"
URL_BASE = "https://api.challonge.com/v2/"


def set_api_key(api_key):
    """Set the challonge.com api credentials to use."""
    _headers["Authorization"] = api_key


def create_tour(tournament_url, tournament_name, is_private=True, is_single_elim=True):
    tournament_type = "single elimination" if is_single_elim else "double elimination"

    url = f"{URL_BASE}tournaments.json"

    data = json.dumps(
        {
            "data": {
                "type": "tournaments",
                "attributes": {
                    "name": tournament_name,
                    "tournament_type": tournament_type,
                    "private": is_private,
                    "url": tournament_url,
                },
            }
        }
    )

    r = requests.post(url, headers=_headers, data=data)
    r.raise_for_status()


# Assumes a list of names of participants, ordered by seed,
# better participant (ie seed #1) first.
def bulk_add_participants(tournament_url, participants):
    url = f"{URL_BASE}tournaments/{tournament_url}/participants/bulk_add.json"

    data = json.dumps(
        {
            "data": {
                "type": "Participant",
                "attributes": {
                    "participants": participants,
                },
            }
        }
    )

    r = requests.post(url, headers=_headers, data=data)
    r.raise_for_status()


def start_tour(tournament_url):
    url = f"{URL_BASE}tournaments/{tournament_url}/change_state.json"

    data = json.dumps(
        {"data": {"type": "TournamentState", "attributes": {"state": "start"}}}
    )

    r = requests.put(url, headers=_headers, data=data)
    r.raise_for_status()


def get_tour(tournament_url):
    url = f"{URL_BASE}tournaments/{tournament_url}.json"

    r = requests.get(url, headers=_headers)
    r.raise_for_status()
    return r.content
