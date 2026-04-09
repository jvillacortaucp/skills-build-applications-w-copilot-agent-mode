from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Borrar datos existentes
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Crear equipos
        marvel = Team.objects.create(name='marvel', description='Marvel Team')
        dc = Team.objects.create(name='dc', description='DC Team')


        # Crear usuarios
        users = [
            User(name='Iron Man', email='ironman@marvel.com', team='marvel'),
            User(name='Captain America', email='cap@marvel.com', team='marvel'),
            User(name='Spider-Man', email='spiderman@marvel.com', team='marvel'),
            User(name='Batman', email='batman@dc.com', team='dc'),
            User(name='Superman', email='superman@dc.com', team='dc'),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team='dc'),
        ]
        for user in users:
            user.save()

        # Crear actividades usando user_email
        Activity.objects.create(user_email='ironman@marvel.com', type='run', duration=30, date='2023-01-01')
        Activity.objects.create(user_email='cap@marvel.com', type='cycle', duration=45, date='2023-01-02')
        Activity.objects.create(user_email='batman@dc.com', type='swim', duration=60, date='2023-01-03')

        # Crear leaderboard usando team_name
        Leaderboard.objects.create(team_name='marvel', points=150)
        Leaderboard.objects.create(team_name='dc', points=120)

        # Crear workouts
        Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='easy')
        Workout.objects.create(name='Squats', description='Do 30 squats', difficulty='medium')
        Workout.objects.create(name='Plank', description='Hold plank for 1 min', difficulty='hard')


        # Crear índice único en email usando pymongo
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.user.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
