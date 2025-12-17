from django.db import models

class Element(models.Model):

    type = models.CharField(max_length=50)