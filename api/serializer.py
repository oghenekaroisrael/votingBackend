from rest_framework import serializers
from .models import Candidate, Poll, Election, Vote


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class VoteResultSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateField()
    election = serializers.CharField()
    status = serializers.CharField()
    user = serializers.CharField()

