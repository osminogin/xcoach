from django.conf.urls import url
from .views import EventList, EventDetail

urlpatterns = [
    url(r'^$', EventList.as_view(), name='event_list'),
    url(r'^(?P<pk>\d+)/$', EventDetail.as_view(), name='event_detail'),
]
