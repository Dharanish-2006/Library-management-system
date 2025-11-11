from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('books/', book_list, name='book_list'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('students/', student_list, name='student_list'),
    path('issue/', issue_book, name='issue_book'),
    path('return/<int:issue_id>/', return_book, name='return_book'),
    path('reports/', reports, name='reports'),
]
