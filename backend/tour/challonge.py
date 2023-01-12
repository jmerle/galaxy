# An API-esque module for our usage.
# Commands here are not very generic (like a good API),
# and are instead tailored to Battlecode's specific usage,
# to improve dev efficiency

# TODO in every method with an api call,
# catch exceptions and throw a new exception if necessary,
# and also kill flow of tour run

import json

import requests

_headers = {
    "Accept": "application/json",
    "Authorization-Type": "v1",
    "Authorization": None,
    "Content-Type": "application/vnd.api+json",
    # requests' default user agent causes Challonge's API to crash.
    "User-Agent": "",
}

AUTH_TYPE = "v1"
URL_BASE = "https://api.challonge.com/v2/"


def set_api_key(api_key):
    """Set the challonge.com api credentials to use."""
    _headers["Authorization"] = api_key


def create_tour(tour_url, tour_name, is_private=True, is_single_elim=True):
    tournament_type = "single elimination" if is_single_elim else "double elimination"

    url = f"{URL_BASE}tournaments.json"

    data = json.dumps(
        {
            "data": {
                "type": "tournaments",
                "attributes": {
                    "name": tour_name,
                    "tournament_type": tournament_type,
                    "private": is_private,
                    "url": tour_url,
                },
            }
        }
    )

    r = requests.post(url, headers=_headers, data=data)
    print(r.status_code)


# Assumes a list of names of participants, ordered by seed,
# better participant (ie seed #1) first.
def bulk_add_participants(tour_url, participants):
    url = f"{URL_BASE}tournaments/{tour_url}/participants/bulk_add.json"

    # Format into what Challonge API wants
    # make sure to change from 0-idx to 1-idx
    participants_formatted = [
        {"name": name, "seed": idx + 1} for (idx, name) in enumerate(participants)
    ]

    data = json.dumps(
        {
            "data": {
                "type": "Participant",
                "attributes": {
                    "participants": participants_formatted,
                },
            }
        }
    )

    r = requests.post(url, headers=_headers, data=data)
    print(r.status_code)


def start_tour(tour_url):
    url = f"{URL_BASE}tournaments/{tour_url}/change_state.json"

    data = json.dumps(
        {"data": {"type": "TournamentState", "attributes": {"state": "start"}}}
    )

    r = requests.put(url, headers=_headers, data=data)
    print(r.status_code)


def get_tour(tour_url):
    url = f"{URL_BASE}tournaments/{tour_url}.json"

    r = requests.get(url, headers=_headers)
    print(r.status_code)
    return r.content
