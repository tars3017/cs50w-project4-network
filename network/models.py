from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

# class comment(models.Model):
#     author = models.ForeignKey("User", on_delete=models.CADCADE, related_name="comment_by"),

class Profile(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="who")
    followers = models.IntegerField(default=0)
    follow_to = models.ManyToManyField("User", blank=True, related_name="follow_who")

    def __str__(self):
        return f"{self.owner.username}'s profile"

    def serialize(self):
        return {
            "followers": self.followers,
            "floowing": self.follow_to
        }

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="from_who")
    content = models.TextField(blank=True, default='')
    like_num = models.IntegerField()
    post_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: {self.poster} {self.post_time}"

    def serialize(slef):
        return {
            "poster": self.poster.username,
            "content": self.content,
            "like_num": self.like_num,
            "post_time": self.post_time.strftime("%b %d %Y, %I:%M %p"),
        }
