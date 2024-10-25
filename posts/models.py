from django.db import models
from django.conf import settings


class Statuses(models.TextChoices):
    """
    Choices for the status of a post or comment.
    """

    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    BLOCKED = "blocked", "Blocked"


class Post(models.Model):
    """
    Model representing a post.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=Statuses.choices, default=Statuses.PENDING
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Model representing a comment.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=Statuses.choices, default=Statuses.PENDING
    )

    def __str__(self):
        return f"{self.author}: {self.content}"
