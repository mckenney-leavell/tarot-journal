from django.db import models
from django.contrib.auth.models import User

class Spread(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=200,
        default='Untitled Spread'
    )

    created_date = models.DateField(
        default="0000-00-00",
    )

    interpretation = models.TextField()