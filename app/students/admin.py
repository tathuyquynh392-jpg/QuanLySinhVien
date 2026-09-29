from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_code",
        "full_name",
        "class_name",
        "major",
        "email",
        "phone",
    )

    search_fields = (
        "student_code",
        "full_name",
        "class_name",
        "major",
        "email",
    )