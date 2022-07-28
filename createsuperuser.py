import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Create the initial admin user'

    def handle(self, *args, **options):
        if User.objects.filter(username="admin").exists():
            print('Admin user already exists.')
            sys.exit(0)
        else:
            user = User.objects.create_superuser(
                username="admin",
                email="minhoteca@livrosviajantes.com.br",
                password="S3nh@root")
            if user:
                print('Admin user created successfully.')
                sys.exit(0)
            else:
                print('Admin user creation failed.')
                sys.exit(1)