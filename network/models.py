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
    like_post = models.ManyToManyField("Post", blank=True, related_name="like_list")

    def __str__(self):
        return self.owner.username

    def serialize(self):
        return {
            "followers": self.followers,
            "floowing": self.follow_to,
            "like": self.like_post,
        }

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="from_who")
    content = models.TextField(blank=True, default='')
    like_num = models.IntegerField()
    post_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}: {self.poster} {self.post_time}"

    def serialize(self, cur_user):
        like_ctl = False
        for fan in self.like_list.all():
            if fan.owner == cur_user:
                like_ctl = True
                break
            print("what?", type(fan), type(cur_user), fan.owner==cur_user)
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "like_num": self.like_num,
            "post_time": self.post_time.strftime("%b %d %Y, %I:%M %p"),
            "is_like": like_ctl,
        }
