from django.shortcuts import render
from .models import *


def index(request):
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
    }
    return render(request, "index.html", context=context)


from django.views.generic import ListView, DetailView


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class BookListView(ListView):
    model = Book
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book
