"""
Tests for Expense views.
"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date

from expenses.models import Expense, ExpenseCategory


@pytest.mark.django_db
class TestExpenseListView:
    """Test cases for the ExpenseListView."""

    def test_expense_list_requires_login(self, client):
        """Test that expense list requires authentication."""
        url = reverse('expense_list')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_expense_list_displays_user_expenses(self, authenticated_client, user):
        """Test that expense list shows only user's expenses."""
        # Create expenses for the authenticated user
        Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        
        # Create expense for another user
        other_user = User.objects.create_user(
            username='other',
            password='otherpass'
        )
        Expense.objects.create(
            user=other_user,
            amount=Decimal('100.00'),
            category=ExpenseCategory.BILLS,
            date=date.today()
        )
        
        url = reverse('expense_list')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert len(response.context['expenses']) == 1
        assert response.context['expenses'][0].user == user

    def test_expense_list_category_filter(self, authenticated_client, user):
        """Test filtering expenses by category."""
        Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        Expense.objects.create(
            user=user,
            amount=Decimal('30.00'),
            category=ExpenseCategory.TRANSPORT,
            date=date.today()
        )
        
        url = reverse('expense_list')
        response = authenticated_client.get(url, {'category': ExpenseCategory.FOOD})
        
        assert response.status_code == 200
        assert len(response.context['expenses']) == 1
        assert response.context['expenses'][0].category == ExpenseCategory.FOOD


@pytest.mark.django_db
class TestExpenseCreateView:
    """Test cases for the ExpenseCreateView."""

    def test_create_expense_requires_login(self, client):
        """Test that creating expense requires authentication."""
        url = reverse('add_expense')
        response = client.get(url)
        assert response.status_code == 302

    def test_create_expense_get(self, authenticated_client):
        """Test GET request to create expense form."""
        url = reverse('add_expense')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_create_expense_post_valid(self, authenticated_client, user):
        """Test creating expense with valid data."""
        url = reverse('add_expense')
        data = {
            'amount': '75.50',
            'category': ExpenseCategory.SHOPPING,
            'date': date.today().isoformat(),
            'description': 'New shoes'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 302
        assert Expense.objects.count() == 1
        expense = Expense.objects.first()
        assert expense.user == user
        assert expense.amount == Decimal('75.50')

    def test_create_expense_post_invalid(self, authenticated_client):
        """Test creating expense with invalid data."""
        url = reverse('add_expense')
        data = {
            'amount': '',  # Missing required field
            'category': ExpenseCategory.FOOD,
            'date': date.today().isoformat()
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 200
        assert Expense.objects.count() == 0
        assert 'form' in response.context
        assert response.context['form'].errors


@pytest.mark.django_db
class TestExpenseUpdateView:
    """Test cases for the ExpenseUpdateView."""

    def test_update_expense_requires_login(self, client, user):
        """Test that updating expense requires authentication."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('edit_expense', kwargs={'pk': expense.pk})
        response = client.get(url)
        assert response.status_code == 302

    def test_update_expense_get(self, authenticated_client, user):
        """Test GET request to update expense form."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('edit_expense', kwargs={'pk': expense.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].instance == expense

    def test_update_expense_post_valid(self, authenticated_client, user):
        """Test updating expense with valid data."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('edit_expense', kwargs={'pk': expense.pk})
        data = {
            'amount': '60.00',
            'category': ExpenseCategory.TRANSPORT,
            'date': date.today().isoformat(),
            'description': 'Updated description'
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == 302
        expense.refresh_from_db()
        assert expense.amount == Decimal('60.00')
        assert expense.category == ExpenseCategory.TRANSPORT

    def test_update_other_user_expense_forbidden(self, authenticated_client):
        """Test that users cannot update other users' expenses."""
        other_user = User.objects.create_user(
            username='other',
            password='otherpass'
        )
        expense = Expense.objects.create(
            user=other_user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('edit_expense', kwargs={'pk': expense.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestExpenseDeleteView:
    """Test cases for the ExpenseDeleteView."""

    def test_delete_expense_requires_login(self, client, user):
        """Test that deleting expense requires authentication."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('delete_expense', kwargs={'pk': expense.pk})
        response = client.get(url)
        assert response.status_code == 302

    def test_delete_expense_get(self, authenticated_client, user):
        """Test GET request to delete confirmation page."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('delete_expense', kwargs={'pk': expense.pk})
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert 'expense' in response.context

    def test_delete_expense_post(self, authenticated_client, user):
        """Test deleting expense."""
        expense = Expense.objects.create(
            user=user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('delete_expense', kwargs={'pk': expense.pk})
        response = authenticated_client.post(url)
        
        assert response.status_code == 302
        assert Expense.objects.count() == 0

    def test_delete_other_user_expense_forbidden(self, authenticated_client):
        """Test that users cannot delete other users' expenses."""
        other_user = User.objects.create_user(
            username='other',
            password='otherpass'
        )
        expense = Expense.objects.create(
            user=other_user,
            amount=Decimal('50.00'),
            category=ExpenseCategory.FOOD,
            date=date.today()
        )
        url = reverse('delete_expense', kwargs={'pk': expense.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestSignUpView:
    """Test cases for the SignUpView."""

    def test_signup_get(self, client):
        """Test GET request to signup form."""
        url = reverse('signup')
        response = client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context

    def test_signup_post_valid(self, client):
        """Test creating new user account."""
        url = reverse('signup')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = client.post(url, data)
        
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()

    def test_signup_redirects_authenticated_user(self, authenticated_client):
        """Test that authenticated users are redirected."""
        url = reverse('signup')
        response = authenticated_client.get(url)
        assert response.status_code == 302
