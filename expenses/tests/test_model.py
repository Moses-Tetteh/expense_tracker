"""
Tests for Expense models.
"""
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from expenses.models import Expense, ExpenseCategory


@pytest.mark.django_db
class TestExpenseModel:
    """Test cases for the Expense model."""

    def test_create_expense(self, user):
        """Test creating a valid expense."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today(),
            description='Lunch at restaurant'
        )
        assert expense.id is not None
        assert expense.user == user
        assert expense.amount == Decimal('50.00')
        assert expense.category == ExpenseCategory.FOOD

    def test_expense_str_representation(self, user):
        """Test the string representation of an expense."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('25.50'),
            category=ExpenseCategory.TRANSPORT,
            date=date.today()
        )
        expected = f"{user.username} - $25.50 (Transportation)"
        assert str(expense) == expected

    def test_expense_ordering(self, user):
        """Test that expenses are ordered by date descending."""
        from datetime import timedelta
        
        expense1 = Expense.objects.create(
            user=user,
            amount=Decimal('10.00'),
            category=ExpenseCategory.FOOD,
            date=date.today() - timedelta(days=2)
        )
        expense2 = Expense.objects.create(
            user=user,
            amount=Decimal('20.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        expense3 = Expense.objects.create(
            user=user,
            amount=Decimal('15.00'),
            category=ExpenseCategory.FOOD,
            date=date.today() - timedelta(days=1)
        )
        
        expenses = list(Expense.objects.all())
        assert expenses[0] == expense2
        assert expenses[1] == expense3
        assert expenses[2] == expense1

    def test_negative_amount_validation(self, user):
        """Test that negative amounts are not allowed."""
        expense = Expense(
            user=user,
            amount=Decimal('-10.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        with pytest.raises(ValidationError):
            expense.full_clean()

    def test_user_relationship(self, user):
        """Test the user relationship and related_name."""
        Expense.objects.create(
            user=user,
            amount=Decimal('100.00'),
            category=ExpenseCategory.BILLS,
            date=date.today()
        )
        assert user.expenses.count() == 1
        assert user.expenses.first().amount == Decimal('100.00')

    def test_category_choices(self, user):
        """Test that only valid category choices are accepted."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('30.00'),
            category=ExpenseCategory.ENTERTAINMENT,
            date=date.today()
        )
        assert expense.category in dict(ExpenseCategory.choices)

    def test_timestamps(self, user):
        """Test that created_at and updated_at are set correctly."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('15.00'),
            category=ExpenseCategory.OTHER,
            date=date.today()
        )
        assert expense.created_at is not None
        assert expense.updated_at is not None
        
        # Update the expense
        original_created = expense.created_at
        expense.amount = Decimal('20.00')
        expense.save()
        expense.refresh_from_db()
        
        assert expense.created_at == original_created
        assert expense.updated_at > expense.created_at
