from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Expense
from .forms import ExpenseForm, SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date', '-id')

    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    if category and category != "All":
        expenses = expenses.filter(category=category)

    if date_from:
        expenses = expenses.filter(date__gte=date_from)

    if date_to:
        expenses = expenses.filter(date__lte=date_to)


    context = {
        'expenses': expenses,
        'selected_category': category,
        'date_from': date_from,
        'date_to': date_to,
        'categories': [
            'Food', 'Transport', 'Shopping', 'Bills', 'Other'
        ]
    }

    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully.")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated.")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted.")
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})
