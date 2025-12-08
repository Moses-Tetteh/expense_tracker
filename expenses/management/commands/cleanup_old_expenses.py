"""
Management command to clean up old expenses.
Usage: python manage.py cleanup_old_expenses --days=365
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from expenses.models import Expense


class Command(BaseCommand):
    help = 'Delete expenses older than specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Delete expenses older than this many days'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']

        cutoff_date = timezone.now().date() - timedelta(days=days)
        old_expenses = Expense.objects.filter(date__lt=cutoff_date)
        count = old_expenses.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS(f'No expenses older than {days} days found')
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} expenses older than {days} days '
                    f'(before {cutoff_date})'
                )
            )
        else:
            old_expenses.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} expenses older than {days} days'
                )
            )
