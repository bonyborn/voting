# voting/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/positions/', views.get_positions, name='get_positions'),
    path('api/settings/', views.get_settings, name='get_settings'),
    path('api/verify-voter/', views.verify_voter, name='verify_voter'),
    path('api/cast-vote/', views.cast_vote, name='cast_vote'),
    path('api/results/', views.get_results, name='get_results'),
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),
    
    # Admin API endpoints
    path('api/admin/login/', views.admin_login, name='admin_login'),
    path('api/admin/toggle-voting/', views.toggle_voting, name='toggle_voting'),
    path('api/admin/reset/', views.reset_election, name='reset_election'),
]