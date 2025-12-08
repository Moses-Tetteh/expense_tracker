from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class ExpenseCategory(models.TextChoices):
    """Choices for expense categories."""
    FOOD = 'FOOD', 'Food & Dining'
    TRANSPORT = 'TRANSPORT', 'Transportation'
    SHOPPING = 'SHOPPING', 'Shopping'
    BILLS = 'BILLS', 'Bills & Utilities'
    ENTERTAINMENT = 'ENTERTAINMENT', 'Entertainment'
    HEALTHCARE = 'HEALTHCARE', 'Healthcare'
    EDUCATION = 'EDUCATION', 'Education'
    OTHER = 'OTHER', 'Other'
    
    


class Expense(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses',
        help_text='The user who created this expense'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='The expense amount (must be positive)'
    )
    category = models.CharField(
        max_length=50,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.OTHER,
        db_index=True,
        help_text='The category of the expense'
    )
    date = models.DateField(
        default=timezone.now,
        db_index=True,
        help_text='The date when the expense occurred'
    )
    description = models.TextField(
        blank=True,
        max_length=500,
        help_text='Optional description or notes about the expense'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When this expense record was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When this expense record was last updated'
    )

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date', '-created_at']),
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category']),
        ]
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        db_table = 'expenses_expense'

    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.get_category_display()})"

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, user={self.user.username}, "
            f"amount={self.amount}, category={self.category}, date={self.date})>"
        )
