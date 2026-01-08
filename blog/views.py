from types import SimpleNamespace

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import PostForm
from .models import Post


def blog_list(request):
    posts = Post.objects.select_related("author")
    query = request.GET.get("q", "").strip()
    country = request.GET.get("country", "").strip()
    if query:
        posts = posts.filter(title__icontains=query)
    if country:
        posts = posts.filter(country__iexact=country)

    # static_posts = [
    #     SimpleNamespace(
    #         title="Hidden Courtyards of Old Prague",
    #         slug="static-prague-courtyards",
    #         country="Czech Republic",
    #         city_or_region="Prague",
    #         short_description=(
    #             "A visual stroll through the tucked-away passageways and quiet squares "
    #             "that reveal Prague's layered architectural heritage."
    #         ),
    #         hero_image_path="images/prague-old-town-square.jpg",
    #         is_static=True,
    #         created_at=timezone.now(),
    #     ),
    #     SimpleNamespace(
    #         title="The Story in Stone",
    #         slug="static-stone-story",
    #         country="Italy",
    #         city_or_region="Tuscany",
    #         short_description=(
    #             "Two timeless masonry scenes captured in the golden light of Tuscany, "
    #             "showing how history lingers in every arch and facade."
    #         ),
    #         hero_image_path="images/istockphoto-696640698-1024x1024.jpg",
    #         is_static=True,
    #         created_at=timezone.now() - timezone.timedelta(days=1),
    #     ),
    # ]
    static_posts=[]

    filtered_static_posts = static_posts
    if query:
        filtered_static_posts = [
            post
            for post in filtered_static_posts
            if query.lower() in post.title.lower()
        ]
    if country:
        filtered_static_posts = [
            post
            for post in filtered_static_posts
            if post.country.lower() == country.lower()
        ]

    combined_posts = list(posts) + filtered_static_posts
    combined_posts.sort(key=lambda post: post.created_at, reverse=True)

    paginator = Paginator(combined_posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    db_countries = (
        Post.objects.values_list("country", flat=True)
        .order_by("country")
        .distinct()
    )
    countries = sorted({*db_countries, *(post.country for post in static_posts)})
    context = {
        "page_obj": page_obj,
        "query": query,
        "country": country,
        "countries": countries,
    }
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author"), slug=slug)
    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
    post.refresh_from_db(fields=["views"])

    related_posts = (
        Post.objects.filter(country__iexact=post.country)
        .exclude(pk=post.pk)
        .order_by("-created_at")[:6]
    )

    referer = request.META.get("HTTP_REFERER")
    back_url = reverse("blog_list")
    if referer and url_has_allowed_host_and_scheme(referer, {request.get_host()}):
        back_url = referer

    context = {
        "post": post,
        "related_posts": related_posts,
        "back_url": back_url,
    }
    return render(request, "blog/blog_detail.html", context)


class DashboardListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/dashboard_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.select_related("author")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"

    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse("dashboard")
