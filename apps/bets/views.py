from django.views.generic import ListView
from .models import Bet


class BetList(ListView):
    model = Bet
