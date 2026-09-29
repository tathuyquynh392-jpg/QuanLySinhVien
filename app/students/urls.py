from django.urls import path

from . import views


urlpatterns = [
    path("", views.student_list, name="student_list"),
    path("them/", views.student_create, name="student_create"),
    path("sua/<int:student_id>/", views.student_edit, name="student_edit"),
    path("xoa/<int:student_id>/", views.student_delete, name="student_delete"),
]