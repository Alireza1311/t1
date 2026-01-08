from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from blog.models import Post

from .forms import ContactForm


def home(request):
    featured_posts = Post.objects.all()[:6]
    popular_posts = Post.objects.order_by("-views", "-created_at")[:6]
    countries = (
        Post.objects.values_list("country", flat=True)
        .order_by("country")
        .distinct()
    )
    context = {
        "featured_posts": featured_posts,
        "popular_posts": popular_posts,
        "countries": countries,
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We will get back to you soon.")
            return redirect(reverse("contact"))
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
