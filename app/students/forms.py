from django import forms
from .models import Student, Class, Grade

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
            
        ]
        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
            
        }


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            "class_code",
            "class_name",
            "major",
        ]
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            "student",
            "semester",
            "academic_year",
            "score_10",
            "score_4",
            "classification",
        ]

        widgets = {
            "score_10": forms.NumberInput(
                attrs={
                    "min": "0",
                    "max": "10",
                    "step": "0.01",
                    "placeholder": "0 - 10"
                }
            ),

            "score_4": forms.NumberInput(
                attrs={
                    "min": "0",
                    "max": "4",
                    "step": "0.01",
                    "placeholder": "0 - 4"
                }
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "placeholder": "VD: 2025-2026"
                }
            ),
            "classification": forms.HiddenInput(),
        }

    def clean_score_10(self):
        score = self.cleaned_data.get("score_10")

        if score is None:
            return score

        if score < 0:
            raise forms.ValidationError(
                "Điểm hệ 10 không được nhỏ hơn 0."
            )

        if score > 10:
            raise forms.ValidationError(
                "Điểm hệ 10 không được lớn hơn 10."
            )

        return score

    def clean_score_4(self):
        score = self.cleaned_data.get("score_4")

        if score is None:
            return score

        if score < 0:
            raise forms.ValidationError(
                "Điểm hệ 4 không được nhỏ hơn 0."
            )

        if score > 4:
            raise forms.ValidationError(
                "Điểm hệ 4 không được lớn hơn 4."
            )

        return score