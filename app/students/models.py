from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):

    GENDER_CHOICES = [
        ("Nam", "Nam"),
        ("Nữ", "Nữ"),
        ("Khác", "Khác"),
    ]

    student_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã sinh viên"
    )

    full_name = models.CharField(
        max_length=100,
        verbose_name="Họ và tên"
    )

    date_of_birth = models.DateField(
        verbose_name="Ngày sinh"
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="Giới tính"
    )

    class_name = models.CharField(
        max_length=100,
        verbose_name="Lớp học"
    )

    major = models.CharField(
        max_length=100,
        verbose_name="Khoa/Ngành"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email học tập"
    )

    phone = models.CharField(
        max_length=10,
        verbose_name="Số điện thoại"
    )

    average_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Điểm trung bình hệ 10"
    )

    def __str__(self):
        return f"{self.student_code} - {self.full_name}"


class Class(models.Model):

    class_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã lớp"
    )

    class_name = models.CharField(
        max_length=100,
        verbose_name="Tên lớp"
    )

    major = models.CharField(
        max_length=100,
        verbose_name="Khoa"
    )

    def __str__(self):
        return f"{self.class_code} - {self.class_name}"
class Grade(models.Model):

    CLASSIFICATION_CHOICES = [
        ("Xuất sắc", "Xuất sắc"),
        ("Giỏi", "Giỏi"),
        ("Khá", "Khá"),
        ("Trung bình", "Trung bình"),
        ("Yếu", "Yếu"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="grades",
        verbose_name="Sinh viên"
    )

    semester = models.CharField(
        max_length=20,
        verbose_name="Học kỳ"
    )

    academic_year = models.CharField(
    max_length=20,
    default="2025-2026",
    verbose_name="Năm học"
)

    score_10 = models.DecimalField(
    max_digits=4,
    decimal_places=2,
    default=0,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(10),
    ],
    verbose_name="Điểm hệ 10"
)

    score_4 = models.DecimalField(
    max_digits=3,
    decimal_places=2,
    default=0,
    validators=[
        MinValueValidator(0),
        MaxValueValidator(4),
    ],
    verbose_name="Điểm hệ 4"
)

    classification = models.CharField(
    max_length=20,
    choices=CLASSIFICATION_CHOICES,
    default="Khá",
    verbose_name="Xếp loại"
)
def save(self, *args, **kwargs):

    if self.score_10 is not None:

        if self.score_10 >= 8.5:
            self.classification = "Xuất sắc"

        elif self.score_10 >= 7:
            self.classification = "Giỏi"

        elif self.score_10 >= 5.5:
            self.classification = "Khá"

        elif self.score_10 >= 4:
            self.classification = "Trung bình"

        else:
            self.classification = "Yếu"

    super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.student.full_name} - {self.semester} - {self.academic_year}"