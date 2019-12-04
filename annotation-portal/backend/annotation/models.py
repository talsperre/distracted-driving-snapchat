from django.db import models
from videos.models import Video
from django.contrib.auth.models import User

# Create your models here.
class Block(models.Model):
    video = models.OneToOneField(Video,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)

class Annotation(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    annotation = models.CharField(max_length=30)
    width = models.CharField(max_length=100, blank=True)
    depth = models.CharField(max_length=100, blank=True)
    skipped = models.BooleanField(default=False)