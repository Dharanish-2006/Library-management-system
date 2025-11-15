from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return f"{self.user.username} ({self.role})"
    


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('recycled', 'Recycled'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    access_count = models.PositiveIntegerField(default=0)
    recycle_status = models.CharField(max_length=100, default='Not Recycled')

    def __str__(self):
        return self.title


# -------------------------------------------------------------------
# 👩‍🎓 STUDENT MODEL
# -------------------------------------------------------------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    roll_no = models.CharField(max_length=20, unique=True, default="UNKNOWN")
    department = models.CharField(max_length=100, default="General")
    email = models.EmailField(default="default@example.com")

    def __str__(self):
        return f"{self.user.username if self.user else 'NoUser'} - {self.roll_no}"


# -------------------------------------------------------------------
# 📖 ISSUED BOOK MODEL
# -------------------------------------------------------------------
class IssuedBook(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} → {self.student.user.username if self.student.user else 'Unknown'}"

    # Simple fine calculation (₹1/day late)
    def calculate_fine(self):
        if self.return_date and self.return_date < timezone.now().date():
            delta = (timezone.now().date() - self.return_date).days
            self.fine_amount = delta * 1.0
            self.save()

