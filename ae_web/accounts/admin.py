from django.contrib import admin

# Register your models here.
from accounts.models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
