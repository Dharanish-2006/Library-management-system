from django.contrib import admin
from .models import Book, Student, IssuedBook, Profile

# -------------------------------------------------------------------
# 🧑‍💼 PROFILE ADMIN
# -------------------------------------------------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "role")


# -------------------------------------------------------------------
# 📚 BOOK ADMIN
# -------------------------------------------------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "access_count", "recycle_status")
    list_filter = ("status", "recycle_status")
    search_fields = ("title", "author")
    ordering = ("title",)


# -------------------------------------------------------------------
# 👩‍🎓 STUDENT ADMIN
# -------------------------------------------------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_no", "department", "email")
    search_fields = ("user__username", "roll_no", "department")
    ordering = ("roll_no",)


# -------------------------------------------------------------------
# 📖 ISSUED BOOK ADMIN
# -------------------------------------------------------------------
@admin.register(IssuedBook)
class IssuedBookAdmin(admin.ModelAdmin):
    list_display = ("book", "student", "issue_date", "return_date", "fine_amount", "fine_paid")
    list_filter = ("fine_paid", "issue_date")
    search_fields = ("book__title", "student__user__username")
    ordering = ("-issue_date",)
