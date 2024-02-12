from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class CustomUserAdmin(UserAdmin):

    model = MyUser

    list_display = ['email', 'username', 'is_verified', 'is_active', 'is_staff', 'is_paid', 'payment_plan', ]

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (
                'is_verified',
                'is_paid',
                'payment_plan',
            )}),
    )

admin.site.register(MyUser, CustomUserAdmin)
