from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("csrf-token", views.csrf_token, name="csrf-token"),
    path("images/<str:image_name>", views.images, name="images"),
    path("forgot-password", views.forgot_password, name="forgot-password"),
    path("validate-reset-password-token", views.validate_reset_password_token, name="validate-reset-password-token"),
    path("reset-password", views.reset_password, name="reset-password"),
    path("courses/me", views.courses_me, name="courses-me"),
    path("courses/<int:course_id>", views.course_id, name="course-id"),
    path("users/me", views.users_me, name="users-me"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("users/users_messages", views.users_messages, name="users_messages"),
    path("apply_course", views.apply_course, name="apply_course"),
    path("course_search", views.course_search, name="course_search"),
    path("dashboard_courses", views.dashboard_courses, name="dashboard_courses"),
    path("dashboard_quiz", views.dashboard_quiz, name="dashboard_quiz"),
    path("view_course", views.view_course, name="view_course"),
    path("payment", views.payment, name="payment"),
    path("view_classroom", views.view_classroom, name="view_classroom"),
    path("change_information", views.change_information, name="change_information"),
    path("users/users_payments", views.users_payments, name="users_payments"),
    path("message", views.message, name="message"),
]