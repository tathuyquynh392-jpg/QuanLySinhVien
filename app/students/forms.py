from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student

        fields = [
            "student_code",
            "full_name",
            "date_of_birth",
            "gender",
            "class_name",
            "major",
            "email",
            "phone",
            "average_score",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "average_score": forms.NumberInput(
                attrs={
                    "min": "0",
                    "max": "10",
                    "step": "0.01",
                    "placeholder": "Nhập điểm trung bình hệ 10"
                }
            ),
        }