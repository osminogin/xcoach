import pytest
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from apps.events.models import Event
from apps.bets.models import Bet
from apps.markets.models import Market


@pytest.fixture
def example_round():
    m = Market.objects.create(name='Match Odds')
    for i in range(0, 2):
        # Create random event series
        e = Event.objects.create(title='Home v Away',
                                 start_time=timezone.now() - timedelta(days=i))
        b = Bet.objects.create(event=e,
                               market=m,
                               balance=settings.MIN_BET*i)
        print(e.id, e.start_time)

    # TODO: Create example betting line
    pass


@pytest.mark.django_db
def test_martingale_strategy(example_round):
    assert True


class TestMartingaleStrategy():
    pass
