from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from pytz import timezone
from betfair import Betfair
from betfair.models import MarketFilter
from apps.events.models import Event


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        # Setup connection to Betfair API-NG
        self.client = Betfair(settings.BETFAIR_APP, settings.BETFAIR_CERT)
        self.client.login(settings.BETFAIR_USER, settings.BETFAIR_PASS)

    def handle(self, *args, **kwargs):
        # XXX: Hardcodign
        msk = timezone('Europe/Moscow')

        # Loop over configured targets
        for competition in settings.TARGETS:
            cid = self.get_competition_id(competition)

            # Get event list for each target team
            for target in settings.TARGETS[competition]:
                events = self.client.list_events(
                    MarketFilter(text_query=target, competition_ids=cid)
                )
                # Event processing
                for e in events:
                    tz = timezone(e.event.timezone)
                    event_id = int(e.event.id)
                    start_time = tz.localize(e.event.open_date).astimezone(msk)
                    # Save persistent data
                    try:
                        event = Event.objects.create(id=event_id,
                                                     title=e.event.name,
                                                     start_time=start_time)
                        event.save()
                        self.stdout.write('Event #%d \'%s\' saved' % (event.id,
                                                                      event.title))
                    except IntegrityError:
                        pass

    def get_competition_id(self, name):
        competitions = self.client.list_competitions(
            MarketFilter(text_query=name)
        )
        for obj in competitions:
            return obj.competition.id
