from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class Book(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("issued", "Issued"),
        ("lost", "Lost"),
    ]

    book_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    access_count = models.PositiveIntegerField(default=0)
    recycle_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)

    def mark_accessed(self):
        self.access_count = models.F('access_count') + 1
        self.last_accessed = timezone.now()
        self.save(update_fields=['access_count', 'last_accessed'])

    def __str__(self):
        return f"{self.title} ({self.book_id})"

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='issues')
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)
    fine_paid = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    DAILY_FINE = 1.00  # currency units per day - change as required

    @property
    def is_returned(self):
        return self.returned_at is not None

    def days_overdue(self, as_of=None):
        if not as_of:
            as_of = timezone.now().date()
        if self.returned_at:
            compare_date = self.returned_at.date()
        else:
            compare_date = as_of
        overdue = (compare_date - self.due_date).days
        return max(0, overdue)

    def calculate_fine(self, as_of=None):
        days = self.days_overdue(as_of=as_of)
        return days * self.DAILY_FINE

    def mark_returned(self):
        if not self.returned_at:
            self.returned_at = timezone.now()
            fine = self.calculate_fine()
            self.fine_paid = fine
            self.save()
            # update book status
            b = self.book
            b.status = 'available'
            b.mark_accessed()
            b.save()
            return fine
        return 0

    def save(self, *args, **kwargs):
        # keep book status consistent
        super().save(*args, **kwargs)
        if not self.returned_at:
            self.book.status = 'issued'
            self.book.save()