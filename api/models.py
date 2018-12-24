from django.db import models
from django.utils import timezone


# Create your models here.


class Post(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def get_tags(self):
        return list(map(lambda i: i.strip(), str(self.tags).split(',')))

    def __str__(self):
        return self.title


class Comment(models.Model):
    idx = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, models.CASCADE)
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return '[{}]: {} - {}'.format(self.post, self.author, self.content)
