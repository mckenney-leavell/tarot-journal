from django.db import models
from .card import Card
from .spread import Spread

class SpreadCard(models.Model):

    card = models.ForeignKey(
        Card,
        on_delete=models.DO_NOTHING,
    )

    spread = models.ForeignKey(
        Spread,
        on_delete=models.DO_NOTHING,
    )