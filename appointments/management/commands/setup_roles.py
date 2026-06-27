"""
Management command to setup initial user roles and groups for Meditrack.

Usage:
    python manage.py setup_roles
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from appointments.models import Appointment
from doctors.models import Doctor
from medications.models import Medication
from records.models import Record


class Command(BaseCommand):
    help = 'Setup initial user roles and groups for Meditrack'

    def handle(self, *args, **options):
        # Define roles
        roles = ['admin', 'doctor', 'receptionist', 'patient']
        
        # Create groups
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created group: {role}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'✓ Group already exists: {role}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Role setup complete!')
        )
        self.stdout.write(
            self.style.WARNING('\nNext steps:')
        )
        self.stdout.write('1. Go to /admin/')
        self.stdout.write('2. Navigate to Users and create test users')
        self.stdout.write('3. Assign each user to a role group')
        self.stdout.write('4. Test the API with each role')
