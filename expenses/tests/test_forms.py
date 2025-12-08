"""
Tests for Expense forms.
"""
import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from expenses.forms import ExpenseForm, SignUpForm
from expenses.models import ExpenseCategory


@pytest.mark.django_db
class TestExpenseForm:
    """Test cases for the ExpenseForm."""

    def test_valid_form(self):
        """Test form with valid data."""
        data = {
            'amount': '50.00',
            'category': ExpenseCategory.FOOD,
            'date': date.today(),
            'description': 'Test expense'
        }
        form = ExpenseForm(data=data)
        assert form.is_valid()

    def test_missing_required_fields(self):
        """Test form with missing required fields."""
        data = {
            'description': 'Test expense'
        }
        form = ExpenseForm(data=data)
        assert not form.is_valid()
        assert 'amount' in form.errors
        assert 'category' in form.errors
        assert 'date' in form.errors

    def test_negative_amount(self):
        """Test form with negative amount."""
        data = {
            'amount': '-50.00',
            'category': ExpenseCategory.FOOD,
            'date': date.today(),
        }
        form = ExpenseForm(data=data)
        assert not form.is_valid()

    def test_form_fields_widgets(self):
        """Test that form fields have proper widgets."""
        form = ExpenseForm()
        assert 'class' in form.fields['amount'].widget.attrs
        assert 'class' in form.fields['category'].widget.attrs
        assert 'class' in form.fields['date'].widget.attrs
        assert 'class' in form.fields['description'].widget.attrs


@pytest.mark.django_db
class TestSignUpForm:
    """Test cases for the SignUpForm."""

    def test_valid_signup_form(self):
        """Test signup form with valid data."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=data)
        assert form.is_valid()

    def test_password_mismatch(self):
        """Test signup form with mismatched passwords."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complexpass123',
            'password2': 'differentpass123'
        }
        form = SignUpForm(data=data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_missing_email(self):
        """Test signup form with missing email."""
        data = {
            'username': 'testuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=data)
        assert not form.is_valid()
        assert 'email' in form.errors

    def test_duplicate_username(self):
        """Test signup form with existing username."""
        User.objects.create_user(
            username='existinguser',
            password='password123'
        )
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = SignUpForm(data=data)
        assert not form.is_valid()
        assert 'username' in form.errors
