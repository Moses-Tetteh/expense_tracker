"""
Management command to export expenses to CSV.
Usage: python manage.py export_expenses --user=username --output=expenses.csv
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import csv
from pathlib import Path

from expenses.models import Expense


class Command(BaseCommand):
    help = 'Export user expenses to CSV file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username to export expenses for'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='expenses.csv',
            help='Output CSV file path'
        )

    def handle(self, *args, **options):
        username = options['user']
        output_file = options['output']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        expenses = Expense.objects.filter(user=user).order_by('-date')

        if not expenses.exists():
            self.stdout.write(
                self.style.WARNING(f'No expenses found for user {username}')
            )
            return

        # Export to CSV
        output_path = Path(output_file)
        with output_path.open('w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Amount', 'Category', 'Description'])

            for expense in expenses:
                writer.writerow([
                    expense.date,
                    expense.amount,
                    expense.get_category_display(),
                    expense.description
                ])

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully exported {expenses.count()} expenses to {output_file}'
            )
        )
