
from django.db import models
from accounts.models import Profile

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'post name: {self.post}, comment id: {self.id}'



