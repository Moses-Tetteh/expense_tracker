"""
Management command to generate sample expense data for testing.
Usage: python manage.py generate_test_data [--users=N] [--expenses=N]
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date, timedelta
import random

from expenses.models import Expense, ExpenseCategory


class Command(BaseCommand):
    help = 'Generate test data for expenses app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of test users to create'
        )
        parser.add_argument(
            '--expenses',
            type=int,
            default=50,
            help='Number of expenses per user'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_expenses = options['expenses']

        self.stdout.write('Generating test data...')

        # Create users
        users = []
        for i in range(num_users):
            username = f'testuser{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='testpass123'
                )
                users.append(user)
                self.stdout.write(f'Created user: {username}')
            else:
                users.append(User.objects.get(username=username))

        # Create expenses
        categories = list(ExpenseCategory.values)
        descriptions = [
            'Grocery shopping',
            'Gas station',
            'Restaurant dinner',
            'Coffee shop',
            'Online shopping',
            'Uber ride',
            'Electricity bill',
            'Movie tickets',
            'Gym membership',
            'Book purchase',
        ]

        total_created = 0
        for user in users:
            for _ in range(num_expenses):
                days_ago = random.randint(0, 90)
                expense_date = date.today() - timedelta(days=days_ago)
                
                Expense.objects.create(
                    user=user,
                    amount=Decimal(str(round(random.uniform(5, 500), 2))),
                    category=random.choice(categories),
                    date=expense_date,
                    description=random.choice(descriptions)
                )
                total_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(users)} users and {total_created} expenses'
            )
        )
