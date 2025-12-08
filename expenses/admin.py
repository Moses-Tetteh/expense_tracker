"""
Admin configuration for expenses app.
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Expense, ExpenseCategory


class ExpenseAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Expense model."""
    
    list_display = [
        'id', 'user', 'formatted_amount', 'category_badge', 
        'date', 'created_at'
    ]
    list_filter = ['category', 'date', 'created_at', 'user']
    search_fields = ['user__username', 'description', 'amount']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Expense Information', {
            'fields': ('user', 'amount', 'category', 'date')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def formatted_amount(self, obj):
        """Display amount with currency symbol."""
        return format_html('<strong>${}</strong>', obj.amount)
    formatted_amount.short_description = 'Amount'
    formatted_amount.admin_order_field = 'amount'

    def category_badge(self, obj):
        """Display category as colored badge."""
        colors = {
            ExpenseCategory.FOOD: '#28a745',
            ExpenseCategory.TRANSPORT: '#007bff',
            ExpenseCategory.SHOPPING: '#ffc107',
            ExpenseCategory.BILLS: '#dc3545',
            ExpenseCategory.ENTERTAINMENT: '#17a2b8',
            ExpenseCategory.HEALTHCARE: '#e83e8c',
            ExpenseCategory.EDUCATION: '#6f42c1',
            ExpenseCategory.OTHER: '#6c757d',
        }
        color = colors.get(obj.category, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; '
            'padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = 'Category'
    category_badge.admin_order_field = 'category'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    def has_add_permission(self, request):
            return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method == "GET":
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in self.model._meta.fields]
    
    


class ReadOnlyUserAdmin(BaseUserAdmin):
    """Read-only admin for User model."""
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method == "GET":
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in User._meta.fields]


# Customize admin site
admin.site.site_header = "Expense Tracker Administration"
admin.site.site_title = "Expense Tracker Admin"
admin.site.index_title = "Welcome to Expense Tracker Admin"

# Register models
admin.site.unregister(User)
admin.site.register(User, ReadOnlyUserAdmin)
admin.site.register(Expense, ExpenseAdmin)
