from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Avg, Count

from .forms import StudentForm
from .models import Student


def student_list(request):
    students = Student.objects.all().order_by("student_code")

    major = request.GET.get("major", "").strip()
    if major:
        students = students.filter(major=major)

    majors = (
        Student.objects
        .values_list("major", flat=True)
        .distinct()
        .order_by("major")
        
    )
    class_count = Student.objects.values("class_name").distinct().count()
    average_score = students.aggregate(avg=Avg("average_score"))["avg"]
    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "majors": majors,
            "selected_major": major,
            "class_count": class_count,
            "average_score": average_score,
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
        {"form": form},
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
        },
    )


def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {"student": student},
    )