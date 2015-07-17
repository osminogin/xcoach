from django.db import models


class Market(models.Model):
    name = models.TextField(max_length=24, unique=True, blank=False)

    class Meta:
        db_table = 'market_types'
