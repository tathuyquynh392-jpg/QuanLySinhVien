from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count

from .forms import StudentForm, ClassForm, GradeForm
from .models import Student, Class, Grade


# =========================================================
# THỐNG KÊ / DASHBOARD
# =========================================================

def dashboard(request):

    # Tổng số sinh viên
    total_students = Student.objects.count()

    # Tổng số lớp
    class_count = Class.objects.count()

    # Điểm trung bình
    average_score = Student.objects.aggregate(
        avg=Avg("average_score")
    )["avg"]

    # Phân loại học lực
    excellent_count = Student.objects.filter(
        average_score__gte=8.5
    ).count()

    good_count = Student.objects.filter(
        average_score__gte=7,
        average_score__lt=8.5
    ).count()

    average_count = Student.objects.filter(
        average_score__gte=5,
        average_score__lt=7
    ).count()

    weak_count = Student.objects.filter(
        average_score__lt=5
    ).count()

    # Sinh viên theo khoa
    students_by_major = list(
        Student.objects
        .values("major")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Dữ liệu phân loại học lực
    score_distribution = {
        "excellent": excellent_count,
        "good": good_count,
        "average": average_count,
        "weak": weak_count,
    }

    return render(
        request,
        "students/dashboard.html",
        {
            "total_students": total_students,
            "class_count": class_count,
            "average_score": average_score,

            "excellent_count": excellent_count,
            "good_count": good_count,
            "average_count": average_count,
            "weak_count": weak_count,

            "students_by_major": students_by_major,

            # QUAN TRỌNG
            "score_distribution": score_distribution,
        },
    )

    # Sinh viên theo khoa
    students_by_major = list(
    Student.objects
    .values("major")
    .annotate(total=Count("id"))
    .order_by("-total")
)

    score_distribution = {
    "excellent": excellent_count,
    "good": good_count,
    "average": average_count,
    "weak": weak_count,
}

    return render(
        request,
        "students/dashboard.html",
        {
            "total_students": total_students,
            "class_count": class_count,
            "average_score": average_score,

            "excellent_count": excellent_count,
            "good_count": good_count,
            "average_count": average_count,
            "weak_count": weak_count,

            "students_by_major": students_by_major,
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
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

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

    # Tính sĩ số từ danh sách sinh viên
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

def grade_create(request):

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
            "classes": Class.objects.all().order_by("class_name"),
            "students": Student.objects.all().order_by("student_code"),
    
        },
    )


def grade_edit(request, grade_id):

    grade = get_object_or_404(
        Grade,
        id=grade_id
    )

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
            "classes": Class.objects.all().order_by("class_name"),
"students": Student.objects.all().order_by("student_code"),
        },
    )


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