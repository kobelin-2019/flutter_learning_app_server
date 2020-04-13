from django.db import models

# Create your models here.

class TodoItem(models.Model):
    content = models.TextField()

class target(models.Model):
    title = models.TextField()
    details = models.TextField()


class Recommend(models.Model):
    identifier = models.TextField()
    author_name = models.TextField()
    voteup_count = models.IntegerField()
    title = models.TextField()
    details = models.TextField()

class User(models.Model):
    name = models.TextField()
    password = models.TextField()
    photo_id = models.TextField()



















