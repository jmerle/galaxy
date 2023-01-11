#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import random

import challonge

# First, user creates a tour with blank challonge links, and "in progress" is false.

# Then user presses a button to "initialize it"

participants = [str(i + 1) for i in range(6)]  # 1-idx


# TODO Challonge might drop v1 auth soon. Hopefully not during January!
# After IAP, we should move to v2 auth. This might be tricky
# cuz there's no frontend-less auth available, yet...
# but you _can_ insert and store tokens into the backend server
def auth(api_key):
    challonge.set_api_key(api_key)


def initialize(tour_url, tour_name, is_single_elim):
    challonge.create_tour(tour_url, tour_name, True, is_single_elim)


# Sandbox testing
if __name__ == "__main__":
    CHALLONGE_API_KEY = os.getenv("CHALLONGE_API_KEY")
    auth(CHALLONGE_API_KEY)

    IS_SINGLE_ELIM = True

    tour_name = "tour_name_test" + str(random.randint(1, 10000))
    tour_name_private = tour_name + "_private"

    initialize(tour_name_private, tour_name_private, IS_SINGLE_ELIM)
