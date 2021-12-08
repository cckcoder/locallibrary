from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic import ListView, DetailView

from .models import *


@login_required
def index(request):
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.count()
    num_books_exact = Book.objects.filter(title__icontains="a").count()
    title = "Local Library"

    context = {
        "title": title,
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "num_books_exact": num_books_exact,
        "num_visits": num_visits,
    }
    return render(request, "index.html", context=context)


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class BookListView(ListView):
    model = Book
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    models = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed_all.html"
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")
