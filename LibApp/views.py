from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book, Student, IssuedBook, Profile
from .forms import BookForm, IssueForm, ReturnForm
from django.db.models import Sum

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            role = user.profile.role
            messages.success(request, f"Welcome {username}! Logged in as {role.capitalize()}.")
            return redirect("LibApp:dashboard") 
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        r = request.POST.get("role")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("LibApp:login")

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already taken.")
            return redirect("LibApp:login")

        user = User.objects.create_user(username=username, email=email, password=password1)

        profile = Profile.objects.get(user=user)
        profile.role = r
        profile.save()

        if r == "student":
            Student.objects.create(
                user=user,
                roll_no=f"STU{user.id}",
                email=email
            )

        messages.success(request, f"Account created successfully as {r}. Please log in.")
        return redirect("LibApp:login")

    return redirect("LibApp:login")



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("LibApp:login")

@login_required
def dashboard(request):
    role = request.user.profile.role
    books = Book.objects.all()

    if role == "librarian":
        return render(request, "dashboard_librarian.html", {"books": books})
    elif role == "student":
        return render(request, "dashboard_student.html", {"books": books})
    else:
        messages.error(request, "Invalid user role.")
        return redirect("LibApp:logout")

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.save()
    return render(request, "book_detail.html", {"book": book})


@login_required
def add_book(request):
    if request.user.profile.role != "librarian":
        messages.error(request, "Only librarians can add books.")
        return redirect("LibApp:dashboard")

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully!")
            return redirect("LibApp:book_list")
    else:
        form = BookForm()

    return render(request, "book_add.html", {"form": form})


@login_required
def student_list(request):
    if request.user.profile.role != "librarian":
        messages.error(request, "Access denied.")
        return redirect("LibApp:dashboard")

    students = Student.objects.all()
    return render(request, "student_list.html", {"students": students})

@login_required
def issue_book(request):
    if request.user.profile.role != "librarian":
        messages.error(request, "Only librarians can issue books.")
        return redirect("LibApp:dashboard")  

    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issued_book = form.save(commit=False)
            book = issued_book.book
            book.access_count += 1
            book.status = "issued"
            book.save()

            issued_book.save()

            messages.success(request, "Book issued successfully!")
            return redirect("LibApp:book_list")
    else:
        form = IssueForm()

    return render(request, "issue_form.html", {"form": form})



@login_required
def return_book(request):
    if request.user.profile.role != "librarian":
        messages.error(request, "Only librarians can return books.")
        return redirect("LibApp:dashboard")

    if request.method == "POST":
        form = ReturnForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book returned successfully!")
            return redirect("LibApp:book_list")
    else:
        form = ReturnForm()

    return render(request, "return_form.html", {"form": form})


@login_required
def reports_dashboard(request):
    if request.user.profile.role != "librarian":
        messages.error(request, "Access denied.")
        return redirect("LibApp:dashboard")

    total_books = Book.objects.count()
    issued_books = IssuedBook.objects.count()
    total_fines = IssuedBook.objects.aggregate(Sum("fine_amount"))["fine_amount__sum"] or 0

    top_accessed_books = Book.objects.order_by("-access_count")[:5]
    unused_books = Book.objects.filter(access_count=0)

    context = {
        "total_books": total_books,
        "issued_books": issued_books,
        "total_fines": total_fines,
        "top_accessed_books": top_accessed_books,
        "unused_books": unused_books,
    }
    return render(request, "reports_dashboard.html", context)
