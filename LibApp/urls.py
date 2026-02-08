from django.urls import path
from .views import *
app_name="LibApp"
urlpatterns = [
    path("", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard, name="dashboard"),
    path("books/", book_list, name="book_list"),
    path("books/<int:pk>/", book_detail, name="book_detail"),
    path("books/add/", add_book, name="add_book"),

    path("students/", student_list, name="student_list"),
    path("issue/", issue_book, name="issue_book"),
    path("return/", return_book, name="return_book"),

    path("reports/", reports_dashboard, name="reports"),
    path("books/request/<int:book_id>/", request_book, name="request_book"),
    path("requests/", book_requests, name="book_requests"),
    path("requests/manage/<int:request_id>/", manage_request, name="manage_request"),


]