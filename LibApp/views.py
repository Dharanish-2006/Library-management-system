from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone
from .models import Book, Student, Issue
from .forms import BookForm, StudentForm, IssueForm
    
@login_required
def dashboard(request):
    total_books = Book.objects.count()
    issued_books = Book.objects.filter(status='issued').count()
    total_students = Student.objects.count()
    recent_issues = Issue.objects.order_by('-issued_at')[:10]

    # Books with zero access count (unused)
    unused_books = Book.objects.filter(access_count=0).count()

    context = {
        'total_books': total_books,
        'issued_books': issued_books,
        'total_students': total_students,
        'recent_issues': recent_issues,
        'unused_books': unused_books,
    }
    return render(request, 'library_app/dashboard.html', context)

@login_required
def book_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status')
    books = Book.objects.all()
    if q:
        books = books.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(book_id__icontains=q))
    if status:
        books = books.filter(status=status)
    return render(request, 'library_app/book_list.html', {'books': books, 'q': q, 'status': status})

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library_app/book_detail.html', {'book': book})

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'library_app/student_list.html', {'students': students})

@login_required
def issue_book(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            # increment access_count
            issue.book.mark_accessed()
            return redirect('library_app:dashboard')
    else:
        form = IssueForm()
    return render(request, 'library_app/issue_form.html', {'form': form})

@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if request.method == 'POST':
        fine = issue.mark_returned()
        return redirect('library_app:dashboard')
    return render(request, 'library_app/return_form.html', {'issue': issue, 'calculated_fine': issue.calculate_fine()})

@login_required
def reports(request):
    top_books = Book.objects.order_by('-access_count')[:10]
    unused_books = Book.objects.filter(access_count=0)
    fines = Issue.objects.filter(fine_paid__gt=0)
    total_fines = fines.aggregate(total=models.Sum('fine_paid'))['total'] or 0
    context = {
        'top_books': top_books,
        'unused_books': unused_books,
        'total_fines': total_fines,
        'fines': fines,
    }
    return render(request, 'library_app/reports_dashboard.html', context)