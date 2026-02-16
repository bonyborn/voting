from django.shortcuts import render

# Create your views here.
# voting/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
import json

from .models import Position, Candidate, Voter, Vote, ElectionSettings, Feedback

def index(request):
    """Main page view"""
    return render(request, 'voting/index.html')

def get_positions(request):
    """API to get all positions with candidates"""
    positions = Position.objects.prefetch_related('candidates').all()
    data = []
    for position in positions:
        candidates = []
        for candidate in position.candidates.all():
            candidates.append({
                'id': candidate.id,
                'name': candidate.name,
                'photo': candidate.photo,
                'agenda': candidate.agenda
            })
        data.append({
            'id': position.id,
            'title': position.title,
            'candidates': candidates
        })
    return JsonResponse({'positions': data})

def get_settings(request):
    """API to get election settings"""
    settings = ElectionSettings.objects.first()
    if settings:
        return JsonResponse({
            'is_voting_active': settings.is_voting_active,
            'voting_start_date': settings.voting_start_date,
            'voting_end_date': settings.voting_end_date
        })
    return JsonResponse({'is_voting_active': False})

@csrf_exempt
def verify_voter(request):
    """API to verify voter admission number"""
    if request.method == 'POST':
        data = json.loads(request.body)
        admission = data.get('admission_number')
        department = data.get('department')
        
        try:
            voter = Voter.objects.get(admission_number=admission)
            if voter.has_voted:
                return JsonResponse({'success': False, 'error': 'Already voted'})
            return JsonResponse({'success': True, 'voter_id': voter.id})
        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid admission number'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def cast_vote(request):
    """API to cast a vote"""
    if request.method == 'POST':
        # Check if voting is active
        settings = ElectionSettings.objects.first()
        if not settings or not settings.is_voting_active:
            return JsonResponse({'success': False, 'error': 'Voting is closed'})
        
        data = json.loads(request.body)
        admission = data.get('admission_number')
        votes = data.get('votes', [])  # List of {position_id, candidate_id}
        
        try:
            voter = Voter.objects.get(admission_number=admission)
            if voter.has_voted:
                return JsonResponse({'success': False, 'error': 'Already voted'})
            
            # Record each vote
            for vote_data in votes:
                position = Position.objects.get(id=vote_data['position_id'])
                candidate = Candidate.objects.get(id=vote_data['candidate_id'])
                
                Vote.objects.create(
                    voter=voter,
                    candidate=candidate,
                    position=position
                )
            
            # Mark voter as voted
            voter.has_voted = True
            voter.voted_at = timezone.now()
            voter.save()
            
            return JsonResponse({'success': True})
            
        except Voter.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid voter'})
        except (Position.DoesNotExist, Candidate.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid vote data'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def get_results(request):
    """API to get voting results"""
    results = []
    positions = Position.objects.all()
    
    for position in positions:
        candidates_data = []
        total_votes = Vote.objects.filter(position=position).count()
        
        for candidate in position.candidates.all():
            votes = Vote.objects.filter(position=position, candidate=candidate).count()
            percentage = round((votes / total_votes * 100), 1) if total_votes > 0 else 0
            
            candidates_data.append({
                'id': candidate.id,
                'name': candidate.name,
                'votes': votes,
                'percentage': percentage
            })
        
        # Sort candidates by votes
        candidates_data.sort(key=lambda x: x['votes'], reverse=True)
        
        results.append({
            'position_id': position.id,
            'position_title': position.title,
            'candidates': candidates_data,
            'total_votes': total_votes
        })
    
    # Get department breakdown
    departments = Voter.objects.filter(has_voted=True).values('department').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return JsonResponse({
        'results': results,
        'total_voters': Voter.objects.filter(has_voted=True).count(),
        'department_breakdown': list(departments)
    })

@csrf_exempt
def submit_feedback(request):
    """API to submit feedback"""
    if request.method == 'POST':
        data = json.loads(request.body)
        Feedback.objects.create(
            department=data.get('department'),
            message=data.get('message')
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def admin_login(request):
    """Admin login API"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid credentials'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def toggle_voting(request):
    """Admin API to toggle voting status"""
    if request.method == 'POST' and request.user.is_staff:
        data = json.loads(request.body)
        settings = ElectionSettings.objects.first()
        if not settings:
            settings = ElectionSettings.objects.create()
        
        settings.is_voting_active = data.get('active', False)
        settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unauthorized'})

@csrf_exempt
def reset_election(request):
    """Admin API to reset election"""
    if request.method == 'POST' and request.user.is_staff:
        # Delete all votes
        Vote.objects.all().delete()
        
        # Reset voters
        Voter.objects.all().update(has_voted=False, voted_at=None)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unauthorized'})