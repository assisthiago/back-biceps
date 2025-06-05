from django.contrib import admin

from app.core.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
