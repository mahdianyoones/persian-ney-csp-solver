from django.db import models

class Reedpiece(models.Model):
    label = models.CharField(max_length=255)
    length = models.FloatField()
    diam = models.FloatField()
    thickness = models.FloatField()
    roundness = models.FloatField()
    