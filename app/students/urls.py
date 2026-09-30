from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("sinh-vien/", views.student_list, name="student_list"),
    path("them/", views.student_create, name="student_create"),
    path("sua/<int:student_id>/", views.student_edit, name="student_edit"),
    path("xoa/<int:student_id>/", views.student_delete, name="student_delete"),

    path("lop/", views.class_list, name="class_list"),
    path("lop/them/", views.class_create, name="class_create"),
    path("lop/sua/<int:class_id>/", views.class_edit, name="class_edit"),
    path("lop/xoa/<int:class_id>/", views.class_delete, name="class_delete"),

    # ĐIỂM SỐ
path("diem-so/", views.grade_list, name="grade_list"),
path("diem-so/them/", views.grade_create, name="grade_create"),
path("diem-so/sua/<int:grade_id>/", views.grade_edit, name="grade_edit"),
path("diem-so/xoa/<int:grade_id>/", views.grade_delete, name="grade_delete"),
]