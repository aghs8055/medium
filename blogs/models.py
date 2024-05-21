from django.db import models

class Blog(models.Model):
    owner = models.ForeignKey('auth.User', related_name='blogs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)