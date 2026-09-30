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
                format="%Y-%m-%d",
                attrs={
                    "type": "date"
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # =========================
        # LỚP HỌC
        # Lấy dữ liệu từ Quản lý lớp
        # =========================
        class_choices = [
            ("", "— Chọn lớp —")
        ]

        for c in Class.objects.all().order_by("class_name"):
            class_choices.append(
                (
                    c.class_name,
                    f"{c.class_code} - {c.class_name}"
                )
            )

        self.fields["class_name"].widget = forms.Select(
            choices=class_choices
        )

        # =========================
        # KHOA / NGÀNH
        # Lấy dữ liệu từ Quản lý lớp
        # =========================
        major_choices = [
            ("", "— Chọn khoa / ngành —")
        ]

        majors = (
            Class.objects
            .values_list("major", flat=True)
            .distinct()
            .order_by("major")
        )

        for major in majors:
            if major:
                major_choices.append(
                    (major, major)
                )

        self.fields["major"].widget = forms.Select(
            choices=major_choices
        )


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = [
            "class_code",
            "class_name",
            "major",
        ]


class GradeForm(forms.ModelForm):

    major = forms.ChoiceField(
        label="Khoa / Ngành",
        required=True
    )

    class_name = forms.ChoiceField(
        label="Lớp",
        required=True
    )

    class Meta:
        model = Grade
        fields = [
            "major",
            "class_name",
            "student",
            "semester",
            "academic_year",
            "score_10",
            "score_4",
            "classification",
        ]

        widgets = {
            "student": forms.Select(
                attrs={
                    "id": "id_student"
                }
            ),

            "semester": forms.TextInput(
                attrs={
                    "placeholder": "VD: Học kỳ 1"
                }
            ),

            "academic_year": forms.TextInput(
                attrs={
                    "placeholder": "VD: 2025-2026"
                }
            ),

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

            "classification": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # =========================
        # KHOA / NGÀNH
        # Lấy từ bảng Class
        # =========================

        major_choices = [
            ("", "— Chọn khoa / ngành —")
        ]

        majors = (
            Class.objects
            .values_list("major", flat=True)
            .distinct()
            .order_by("major")
        )

        for major in majors:
            if major:
                major_choices.append(
                    (major, major)
                )

        self.fields["major"].choices = major_choices


        # =========================
        # LỚP
        # Lấy từ bảng Class
        # =========================

        class_choices = [
            ("", "— Chọn lớp —")
        ]

        classes = (
            Class.objects
            .all()
            .order_by("class_name")
        )

        for class_obj in classes:
            class_choices.append(
                (
                    class_obj.class_name,
                    f"{class_obj.class_code} - {class_obj.class_name}"
                )
            )

        self.fields["class_name"].choices = class_choices