from django.db import models

class Value(models.Model):

    type = models.CharField(max_length = 50)