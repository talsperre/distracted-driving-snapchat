from django.db import models

# Create your models here.
class Video(models.Model):

    VideoID = models.CharField(max_length=100, unique=True)
    path = models.CharField(max_length=200)
    num_annotations = models.IntegerField(default=0)
