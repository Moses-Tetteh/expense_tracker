from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Expense


class ReadOnlyUserAdmin(BaseUserAdmin):

    
    def has_add_permission(self, request):
        return False

    
    def has_delete_permission(self, request, obj=None):
        return False

    
    def has_change_permission(self, request, obj=None):
        if request.method == "GET":  # view only
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        return [field.name for field in User._meta.fields]


class ExpenseReadOnlyAdmin(admin.ModelAdmin):

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


admin.site.unregister(User)

admin.site.register(User, ReadOnlyUserAdmin)

admin.site.register(Expense, ExpenseReadOnlyAdmin)
