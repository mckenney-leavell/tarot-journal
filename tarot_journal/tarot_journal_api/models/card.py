from django.db import models
from .value import Value
from .element import Element

class Card(models.Model):

    name = models.CharField(
        max_length=250
    )

    value = models.ForeignKey(
        Value, 
        on_delete=models.DO_NOTHING, 
        related_name="cards",
        null=True,
        blank=True
    )

    element = models.ForeignKey(
        Element, 
        on_delete=models.DO_NOTHING, 
        related_name="cards",
        null=True,
        blank=True
    )

    major_arcana = models.BooleanField(default=False)

    meaning_upright = models.TextField()

    meaning_reverse = models.TextField()

    url = models.CharField(null=True)