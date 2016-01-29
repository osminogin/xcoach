from django.utils import timezone
from django.db.models import Sum
from django.views.generic import ListView, DetailView
from lib.teams import find_target_team
from apps.bets.models import Bet
from .models import Event


class EventList(ListView):
    model = Event
    queryset = Event.objects.filter(start_time__gte=timezone.now())


class EventDetail(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        target = find_target_team(context['event'].title)
        context['related_bets'] = Bet.objects.filter(event__title__icontains=target)
        context['total'] = context['related_bets'].aggregate(Sum('balance'))
        return context
