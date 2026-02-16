from django.contrib import admin

# Register your models here.
# voting/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Position, Candidate, Voter, Vote, ElectionSettings, Feedback

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'candidate_count']
    list_editable = ['order']
    search_fields = ['title']
    
    def candidate_count(self, obj):
        return obj.candidates.count()
    candidate_count.short_description = 'Candidates'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'vote_count', 'photo_preview']
    list_filter = ['position']
    search_fields = ['name', 'agenda']
    
    def vote_count(self, obj):
        return obj.vote_set.count()
    vote_count.short_description = 'Votes Received'
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 50px;">', obj.photo)
        return "No photo"
    photo_preview.short_description = 'Photo'

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['admission_number', 'department', 'has_voted', 'voted_at']
    list_filter = ['department', 'has_voted']
    search_fields = ['admission_number']
    date_hierarchy = 'voted_at'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'candidate', 'position', 'voted_at']
    list_filter = ['position', 'voted_at']
    search_fields = ['voter__admission_number', 'candidate__name']
    date_hierarchy = 'voted_at'

@admin.register(ElectionSettings)
class ElectionSettingsAdmin(admin.ModelAdmin):
    list_display = ['is_voting_active', 'voting_start_date', 'voting_end_date', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one settings object
        return not ElectionSettings.objects.exists()

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['department', 'submitted_at', 'message_preview']
    list_filter = ['department', 'submitted_at']
    date_hierarchy = 'submitted_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Feedback'