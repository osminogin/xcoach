from django.db import models
from apps.events.models import Event
from apps.markets.models import Market


class Bet(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True)
    market = models.ForeignKey(Market)
    settled_date = models.DateTimeField(blank=False)
    balance = models.FloatField(blank=False)

    class Meta:
        db_table = 'bets'
        ordering = ['-settled_date']
