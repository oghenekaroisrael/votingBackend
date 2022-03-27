from ast import mod
from datetime import datetime, timezone
from django.db import models
from user.models import User
# Create your models here.

STATUS = [
    ('SCHEDULED', 'Scheduled'),
    ('ONGOING', 'Ongoing'),
    ('COMPLETED', 'Completed'),
    ('PENDING', 'Pending')
]

CANDIDATE_STATUS = [
    ('RUNNING', 'Running'),
    ('DROPPED_OUT', 'Dropped_Out'),
    ('WON', 'WON'),
    ('LOST', 'LOST')
]

class Election(models.Model):
    election_name = models.CharField(max_length=50)
    dateCreated = models.DateField( auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=50)
    creation_date = models.DateField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.poll_name+" "+self.status

class Poll(models.Model):
    poll_name = models.CharField(max_length=50)
    dateCreated = models.DateField( auto_now=True)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.poll_name+" "+self.status

class Candidate(models.Model):
    # candidate_name = models.CharField(default='', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=CANDIDATE_STATUS, max_length=15, blank=True, default=CANDIDATE_STATUS[0], null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self) -> str:
        return self.user

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, blank=True, null=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, blank=True, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, blank=True, null=True)
    vote_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self) -> str:
        return self.user
