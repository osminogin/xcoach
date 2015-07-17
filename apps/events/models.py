from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=50)
    start_time = models.DateTimeField(blank=False)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'events'
        ordering = ['start_time']
