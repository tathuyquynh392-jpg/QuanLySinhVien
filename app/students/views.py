from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count

from .forms import StudentForm, ClassForm, GradeForm
from .models import Student, Class, Grade

import requests


# =========================================================
# PROMETHEUS
# =========================================================

def get_prometheus_value(query):
    try:
        response = requests.get(
            "http://prometheus:9090/api/v1/query",
            params={"query": query},
            timeout=3
        )

        data = response.json()
        result = data.get("data", {}).get("result", [])

        if result:
            return float(result[0]["value"][1])

    except Exception:
        pass

    return 0


# =========================================================
# THỐNG KÊ / DASHBOARD
# =========================================================

def dashboard(request):

    total_students = Student.objects.count()

    class_count = Class.objects.count()

    # Điểm trung bình hệ 4
    average_score = Grade.objects.aggregate(
        avg=Avg("score_4")
    )["avg"]

    # Thống kê xếp loại
    excellent_count = Grade.objects.filter(
        classification="Xuất sắc"
    ).count()

    good_count = Grade.objects.filter(
        classification="Giỏi"
    ).count()

    fair_count = Grade.objects.filter(
        classification="Khá"
    ).count()

    average_count = Grade.objects.filter(
        classification="Trung bình"
    ).count()

    weak_count = Grade.objects.filter(
        classification="Yếu"
    ).count()

    poor_count = Grade.objects.filter(
        classification="Kém"
    ).count()

    # Sinh viên theo khoa
    
    students_by_major = list(
        Student.objects
            .values("major")
            .annotate(total=Count("id"))
            .order_by("major")
    )



    # CPU
    cpu_usage = get_prometheus_value(
        "sum(rate(container_cpu_usage_seconds_total{name!=''}[5m])) * 100"
    )

    # RAM
    ram_usage = get_prometheus_value(
        "sum(container_memory_usage_bytes{name!=''}) / 1024 / 1024"
    )

    return render(
        request,
        "students/dashboard.html",
        {
            "total_students": total_students,
            "class_count": class_count,

            # Điểm trung bình hệ 4
            "average_score": (
                round(float(average_score), 2)
                if average_score is not None
                else 0
            ),

            # Xếp loại
            "excellent_count": excellent_count,
            "good_count": good_count,
            "fair_count": fair_count,
            "average_count": average_count,
            "weak_count": weak_count,
            "poor_count": poor_count,

            # Sinh viên theo khoa
            "students_by_major": students_by_major,

            # Tải máy chủ
            "cpu_usage": round(cpu_usage, 1),
            "ram_usage": round(ram_usage, 1),
        },
    )


# =========================================================
# QUẢN LÝ SINH VIÊN
# =========================================================

def student_list(request):

    students = Student.objects.all().order_by("student_code")

    # Lọc theo khoa
    major = request.GET.get("major", "").strip()

    if major:
        students = students.filter(major=major)

    # Danh sách khoa
    majors = (
        Student.objects
        .values_list("major", flat=True)
        .distinct()
        .order_by("major")
    )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "majors": majors,
            "selected_major": major,
        },
    )


def student_create(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form
        },
    )


def student_edit(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("student_list")

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "student": student,
        }
    )


def student_delete(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student.delete()

        return redirect("student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {
            "student": student
        },
    )


# =========================================================
# QUẢN LÝ LỚP
# =========================================================

def class_list(request):

    classes = Class.objects.all().order_by("class_code")

    # Lọc theo khoa
    major = request.GET.get("major", "").strip()

    if major:
        classes = classes.filter(major=major)

    # Tính sĩ số
    for class_obj in classes:

        class_obj.student_count = Student.objects.filter(
            class_name=class_obj.class_name
        ).count()

    # Danh sách khoa
    majors = (
        Class.objects
        .values_list("major", flat=True)
        .distinct()
        .order_by("major")
    )

    return render(
        request,
        "students/class_list.html",
        {
            "classes": classes,
            "majors": majors,
            "selected_major": major,
        },
    )


def class_create(request):

    if request.method == "POST":

        form = ClassForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("class_list")

    else:

        form = ClassForm()

    return render(
        request,
        "students/class_form.html",
        {
            "form": form
        },
    )


def class_edit(request, class_id):

    class_obj = get_object_or_404(
        Class,
        id=class_id
    )

    if request.method == "POST":

        form = ClassForm(
            request.POST,
            instance=class_obj
        )

        if form.is_valid():
            form.save()
            return redirect("class_list")

    else:

        form = ClassForm(
            instance=class_obj
        )

    return render(
        request,
        "students/class_form.html",
        {
            "form": form,
            "class_obj": class_obj,
        },
    )


def class_delete(request, class_id):

    class_obj = get_object_or_404(
        Class,
        id=class_id
    )

    if request.method == "POST":

        class_obj.delete()

        return redirect("class_list")

    return render(
        request,
        "students/class_confirm_delete.html",
        {
            "class_obj": class_obj,
        },
    )


# =========================================================
# QUẢN LÝ ĐIỂM SỐ
# =========================================================

def grade_list(request):

    grades = (
        Grade.objects
        .select_related("student")
        .order_by(
            "student__student_code",
            "semester",
            "academic_year"
        )
    )

    return render(
        request,
        "students/grade_list.html",
        {
            "grades": grades,
        },
    )


# =========================================================
# THÊM ĐIỂM
# =========================================================

def grade_create(request):

    # Lấy dữ liệu cho JavaScript
    classes = Class.objects.all().order_by("class_name")

    students = Student.objects.all().order_by("student_code")

    if request.method == "POST":

        form = GradeForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("grade_list")

    else:

        form = GradeForm()

    return render(
        request,
        "students/grade_form.html",
        {
            "form": form,

            # QuerySet → list(dict)
            # để json_script có thể chuyển thành JSON
            "classes": list(
                classes.values(
                    "id",
                    "class_name",
                    "major"
                )
            ),

            "students": list(
                students.values(
                    "id",
                    "student_code",
                    "full_name",
                    "class_name",
                    "major"
                )
            ),
        },
    )


# =========================================================
# SỬA ĐIỂM
# =========================================================

def grade_edit(request, grade_id):

    grade = get_object_or_404(
        Grade,
        id=grade_id
    )

    # Dữ liệu cho JavaScript
    classes = Class.objects.all().order_by("class_name")

    students = Student.objects.all().order_by("student_code")

    if request.method == "POST":

        form = GradeForm(
            request.POST,
            instance=grade
        )

        if form.is_valid():

            form.save()

            return redirect("grade_list")

    else:

        form = GradeForm(
            instance=grade
        )

    return render(
        request,
        "students/grade_form.html",
        {
            "form": form,

            "grade": grade,

            # Chuyển QuerySet thành list để json_script sử dụng
            "classes": list(
                classes.values(
                    "id",
                    "class_name",
                    "major"
                )
            ),

            "students": list(
                students.values(
                    "id",
                    "student_code",
                    "full_name",
                    "class_name",
                    "major"
                )
            ),
        },
    )


# =========================================================
# XÓA ĐIỂM
# =========================================================

def grade_delete(request, grade_id):

    grade = get_object_or_404(
        Grade,
        id=grade_id
    )

    if request.method == "POST":

        grade.delete()

        return redirect("grade_list")

    return render(
        request,
        "students/grade_confirm_delete.html",
        {
            "grade": grade,
        },
    )