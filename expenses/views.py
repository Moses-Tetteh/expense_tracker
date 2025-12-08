from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from datetime import datetime, timedelta

from .models import Expense, ExpenseCategory
from .forms import ExpenseForm, SignUpForm


class SignUpView(FormView):
    """Handle user registration."""
    
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to expense list
        if request.user.is_authenticated:
            return redirect('expense_list')
        return super().dispatch(request, *args, **kwargs)


class ExpenseListView(LoginRequiredMixin, ListView):
    """
    Display list of expenses with filtering capabilities.
    Users can filter by category and date range.
    """
    
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 20

    def get_queryset(self):
        """Filter expenses based on query parameters."""
        queryset = Expense.objects.filter(user=self.request.user)

        # Category filter
        category = self.request.GET.get('category')
        if category and category != 'All':
            queryset = queryset.filter(category=category)

        # Date range filter
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(description__icontains=search) |
                Q(amount__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        
        # Pass filter parameters back to template
        context['selected_category'] = self.request.GET.get('category', 'All')
        context['date_from'] = self.request.GET.get('date_from', '')
        context['date_to'] = self.request.GET.get('date_to', '')
        context['search'] = self.request.GET.get('search', '')
        context['categories'] = ExpenseCategory.choices

        # Calculate total for filtered expenses
        context['total_amount'] = self.get_queryset().aggregate(
            total=Sum('amount')
        )['total'] or 0

        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """Handle creation of new expenses."""
    
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        """Set the user before saving."""
        form.instance.user = self.request.user
        messages.success(self.request, 'Expense added successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Expense'
        context['submit_text'] = 'Add Expense'
        return context


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """Handle updating existing expenses."""
    
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense_list')

    def get_queryset(self):
        """Ensure users can only edit their own expenses."""
        return Expense.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Expense'
        context['submit_text'] = 'Update Expense'
        return context


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """Handle deletion of expenses."""
    
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense_list')

    def get_queryset(self):
        """Ensure users can only delete their own expenses."""
        return Expense.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Expense deleted successfully!')
        return super().delete(request, *args, **kwargs)


signup = SignUpView.as_view()
expense_list = ExpenseListView.as_view()
add_expense = ExpenseCreateView.as_view()
edit_expense = ExpenseUpdateView.as_view()
delete_expense = ExpenseDeleteView.as_view()
