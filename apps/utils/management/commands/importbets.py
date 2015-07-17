import re
import xlrd
from datetime import datetime
from collections import Counter
from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
from apps.bets.models import Bet
from apps.events.models import Event
from apps.markets.models import Market


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        # Update data before importing bets
        management.call_command('updatedata')

        # Parse and store bets from Excel file
        with xlrd.open_workbook(options['file']) as book:
            sheet = book.sheet_by_index(0)
            target_team = Counter(self.get_team_list(settings.TARGETS))
            stored = 0

            # Get bets information for each row
            for rownum in range(sheet.nrows):
                # Skip table header
                if rownum in [0, 1]:
                    continue

                # Parse entry data
                row = sheet.row_values(rownum)
                found = re.search(r'/\s(.+)\s:\s(.*)', row[0])
                if found:
                    event_title = found.group(1)
                    market_name = found.group(2)
                start_time = datetime.strptime(row[1], '%d-%b-%y %H:%M ')
                settled_date = datetime.strptime(row[2], '%d-%b-%y %H:%M ')
                balance = row[3]

                # Check only target teams (but warn is not related to competitions)
                home, away = re.split('\sv\s', event_title)
                target = None
                if target_team[home]:
                    target = home
                elif target_team[away]:
                    target = away
                if target is None:
                    continue

                # TODO: Need to handle market types (now only skipping unknown markets)
                if not market_name == 'Match Odds':
                    continue

                # Create related entries if needed
                market, _ = Market.objects.get_or_create(name=market_name)
                event, _ = Event.objects.get_or_create(title=event_title,
                                                       start_time=start_time)

                # Storing bet
                bet, created = Bet.objects.get_or_create(market=market,
                                                         event=event,
                                                         settled_date=settled_date,
                                                         balance=balance)
                if created:
                    stored += 1

        self.stdout.write('%d new bets imported from file %s' % (stored,
                                                                 options['file']))

    @staticmethod
    def get_team_list(targets):
        """ Returns flat teams list from tratgets hash. """
        teams = []
        for key, value in targets.items():
            teams.extend(value)
        return teams
