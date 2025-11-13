from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book, IssuedBook, Student, Profile


# -------------------------------------------------------------------
# 🧾 USER SIGNUP FORM (with role selection)
# -------------------------------------------------------------------
class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    ]
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile with selected role
            role = self.cleaned_data['role']
            Profile.objects.filter(user=user).update(role=role)

            # If student, also create a Student record
            if role == 'student':
                Student.objects.create(
                    user=user,
                    roll_no=f"R{user.id:03d}",
                    department="General",
                    email=user.email
                )
        return user


# -------------------------------------------------------------------
# 📚 BOOK FORM
# -------------------------------------------------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'status', 'recycle_status']


# -------------------------------------------------------------------
# 📖 ISSUE FORM
# -------------------------------------------------------------------
class IssueForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['student', 'book', 'return_date']


# -------------------------------------------------------------------
# 🔁 RETURN FORM
# -------------------------------------------------------------------
class ReturnForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = ['fine_paid']
