# voting/migrations/initial_data.py
from django.db import migrations

def create_initial_data(apps, schema_editor):
    Position = apps.get_model('voting', 'Position')
    Candidate = apps.get_model('voting', 'Candidate')
    Voter = apps.get_model('voting', 'Voter')
    ElectionSettings = apps.get_model('voting', 'ElectionSettings')
    
    # Create positions
    president = Position.objects.create(id='president', title='School President', order=1)
    secretary = Position.objects.create(id='secretary', title='Secretary General', order=2)
    education = Position.objects.create(id='education', title='Cabinet Secretary for Education', order=3)
    
    # Create candidates
    Candidate.objects.create(
        id='alex-johnson',
        name='Boniface Kathu',
        photo='static/',
        agenda='Mental health support, sustainability, transparent budgeting',
        position=president
    )
    Candidate.objects.create(
        id='samuel-brown',
        name='sammy',
        photo='',
        agenda='School spirit, sports funding, cafeteria improvements',
        position=president
    )
    Candidate.objects.create(
        id='jessica-williams',
        name='Jessy',
        photo='',
        agenda='Technology upgrades, club funding, student discounts',
        position=president
    )
    
    Candidate.objects.create(
        id='maria-rodriguez',
        name='precious',
        photo='fgr',
        agenda='Transparent communication, digital archives, mentorship',
        position=secretary
    )
    Candidate.objects.create(
        id='ryan-miller',
        name='Mulwa',
        photo='',
        agenda='Efficient meetings, better minutes, app development',
        position=secretary
    )
    
    Candidate.objects.create(
        id='david-chen',
        name='Mark Vundi',
        photo='static/Mark.jpg',
        agenda='Peer tutoring, digital resources, study skills workshops',
        position=education
    )
    Candidate.objects.create(
        id='sophia-kim',
        name='Kamani',
        photo='no idea',
        agenda='Curriculum diversity, exam support, teacher feedback',
        position=education
    )
    
    # Create voters (students)
    voters = [
        ('NUU001', 'Computing and Informatics'),
        ('NUU002', 'Electrical Engineering'),
        ('NUU003', 'Business and secretarial studies'),
        ('NUU004', 'Automative Engineering'),
        ('NUU005', 'Other'),
    ]
    
    for admission, dept in voters:
        Voter.objects.create(
            admission_number=admission,
            department=dept,
            has_voted=False
        )
    
    # Create election settings
    ElectionSettings.objects.create(
        is_voting_active=False
    )

class Migration(migrations.Migration):
    dependencies = [
        ('voting', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_initial_data),
    ]