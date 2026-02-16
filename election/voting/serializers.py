# voting/serializers.py
from rest_framework import serializers
from .models import Position, Candidate, Voter, Vote, ElectionSettings, Feedback

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'photo', 'agenda']

class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'title', 'candidates']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['voter', 'candidate', 'position']

class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ['admission_number', 'department', 'has_voted']

class ElectionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionSettings
        fields = ['is_voting_active', 'voting_start_date', 'voting_end_date']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['department', 'message']