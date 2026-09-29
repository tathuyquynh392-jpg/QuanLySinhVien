from django.db import models


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