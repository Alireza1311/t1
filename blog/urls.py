from django.urls import path

from . import views

urlpatterns = [
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("dashboard/", views.DashboardListView.as_view(), name="dashboard"),
    path("dashboard/new/", views.PostCreateView.as_view(), name="post_create"),
    path("dashboard/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("dashboard/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
