import re
from collections import Counter
from django.conf import settings


def find_target_team(event_title):
    """ Return target team from event. """
    target_team = Counter(get_team_list(settings.TARGETS))

    # Check only target teams (but warn is not related to competitions)
    home, away = re.split('\sv\s', event_title)
    target = None
    if target_team[home]:
            target = home
    elif target_team[away]:
            target = away

    return target


def get_team_list(targets):
    """ Returns flat teams list from targets hash. """
    teams = []
    for key, value in targets.items():
        teams.extend(value)
    return teams
