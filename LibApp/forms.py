from django import forms
from .models import Book, Student, Issue

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'status', 'recycle_status']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'email', 'phone']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['book', 'student', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }