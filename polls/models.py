from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Question model

class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_published = models.DateTimeField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


# Choices model

class Choices(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    votes = models.IntegerField()

    def __str__(self):
        return self.text


class PollsUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vote_count = models.IntegerField(default=0)
    question_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Question = models.ForeignKey(Poll, on_delete=models.CASCADE)
    Option = models.ForeignKey(Choices, on_delete=models.CASCADE)
    date = models.DateTimeField()


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)



