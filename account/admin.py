from django.contrib import admin

from account.models import AccountUser


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('username', {'fields': ['username']}),
        ('password', {'fields': ['password']}),
        ('email', {'fields': ['email']}),
        ('person_id', {'fields': ['person_id']}),
        ('is_staff', {'fields': ['is_staff']}),
        ('is_active', {'fields': ['is_active']}),
        ('last_login', {'fields': ['last_login']}),
        ('date_joined', {'fields': ['date_joined']}),
    ]
    list_display = ('username', 'password', 'email', 'person_id', 'is_staff', 'is_active', 'last_login', 'date_joined')


admin.site.register(AccountUser, AccountAdmin)


# Register your models here.
