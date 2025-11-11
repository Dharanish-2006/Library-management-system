from django.contrib import admin
from .models import Book, Student, Issue

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'status', 'access_count', 'recycle_status')
    search_fields = ('book_id', 'title', 'author')
    list_filter = ('status', 'recycle_status')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email')
    search_fields = ('student_id', 'name')

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issued_at', 'due_date', 'returned_at', 'fine_paid')
    list_filter = ('issued_at', 'due_date')