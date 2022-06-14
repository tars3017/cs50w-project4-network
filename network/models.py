from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class comment(models.Model):
#     author = models.ForeignKey("User", on_delete=models.CADCADE, related_name="comment_by"),

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="from_who")
    content = models.TextField(blank=True, default='')
    like_num = models.IntegerField()
    post_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: {self.poster} {self.post_time}"
