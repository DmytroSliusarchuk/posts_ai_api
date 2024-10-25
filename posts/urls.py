from django.urls import path

from .views import (
    PostListCreateView,
    PostDetailView,
    CommentListCreateView,
    CommentDetailView,
    CommentsDailyBreakdownView,
)


urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post_list_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "posts/<int:post_id>/comments/",
        CommentListCreateView.as_view(),
        name="comment_list_create",
    ),
    path("comments/<int:pk>/", CommentDetailView.as_view(), name="comment_detail"),
    path(
        "analytics/comments-daily-breakdown/",
        CommentsDailyBreakdownView.as_view(),
        name="comments_daily_breakdown",
    ),
]
