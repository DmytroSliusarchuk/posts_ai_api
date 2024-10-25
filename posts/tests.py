from datetime import datetime, timedelta, timezone

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from unittest.mock import patch

from .models import Post, Comment, Statuses

User = get_user_model()


class PostsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@email.com"
        )
        self.client = APIClient()

        self.patcher_moderate_post_content = patch(
            "posts.views.moderate_post_content.delay"
        )
        self.mock_moderate_post_content_delay = (
            self.patcher_moderate_post_content.start()
        )
        self.addCleanup(self.patcher_moderate_post_content.stop)

        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )

        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_create_post(self):
        url = reverse("post_list_create")
        data = {"title": "Test Post", "content": "This is a test post."}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["author"], self.user.username)
        self.assertEqual(response.data["status"], Statuses.PENDING)

    def test_list_posts(self):
        Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test content",
            status=Statuses.APPROVED,
        )

        url = reverse("post_list_create")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test content",
            status=Statuses.APPROVED,
        )

        url = reverse("post_detail", kwargs={"pk": post.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], post.id)

    def test_update_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Old Title",
            content="Old content",
            status=Statuses.APPROVED,
        )

        url = reverse("post_detail", kwargs={"pk": post.id})
        data = {"title": "New Title", "content": "Updated content"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["content"], data["content"])

    def test_delete_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test content",
            status=Statuses.APPROVED,
        )

        url = reverse("post_detail", kwargs={"pk": post.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())


class CommentsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test2@email.com"
        )
        self.post_author = User.objects.create_user(
            username="postauthor", password="postpass123", email="test3@email.com"
        )
        self.post = Post.objects.create(
            author=self.post_author,
            title="Test Post",
            content="Test content",
            status=Statuses.APPROVED,
        )

        self.patcher_moderate_comment_content = patch(
            "posts.views.moderate_comment_content.delay"
        )
        self.mock_moderate_comment_content_delay = (
            self.patcher_moderate_comment_content.start()
        )
        self.addCleanup(self.patcher_moderate_comment_content.stop)

        self.client = APIClient()
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )

        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_create_comment(self):
        url = reverse("comment_list_create", kwargs={"post_id": self.post.id})
        data = {"content": "This is a test comment."}

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["author"], self.user.username)
        self.assertEqual(response.data["status"], Statuses.PENDING)

    def test_list_comments(self):
        Comment.objects.create(
            author=self.user,
            post=self.post,
            content="Test comment 1",
            status=Statuses.APPROVED,
        )
        Comment.objects.create(
            author=self.user,
            post=self.post,
            content="Test comment 2",
            status=Statuses.APPROVED,
        )

        url = reverse("comment_list_create", kwargs={"post_id": self.post.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_comment(self):
        comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content="Test comment",
            status=Statuses.APPROVED,
        )

        url = reverse("comment_detail", kwargs={"pk": comment.id})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], comment.id)

    def test_update_comment(self):
        comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content="Old content",
            status=Statuses.APPROVED,
        )

        url = reverse("comment_detail", kwargs={"pk": comment.id})
        data = {"content": "Updated content"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], data["content"])

    def test_delete_comment(self):
        comment = Comment.objects.create(
            author=self.user,
            post=self.post,
            content="Test comment",
            status=Statuses.APPROVED,
        )

        url = reverse("comment_detail", kwargs={"pk": comment.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())


class AnalyticsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test4@email.com"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post",
            content="Test content",
            status=Statuses.APPROVED,
        )
        self.client = APIClient()

        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )

        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        today = datetime.now(timezone.utc)
        for i in range(5):
            created_at = today - timedelta(days=i)
            comment = Comment.objects.create(
                author=self.user,
                post=self.post,
                content=f"Test comment {i}",
                status=Statuses.APPROVED,
            )
            comment.created_at = created_at
            comment.save()

            if i % 2 == 0:
                blocked_comment = Comment.objects.create(
                    author=self.user,
                    post=self.post,
                    content=f"Blocked comment {i}",
                    status=Statuses.BLOCKED,
                )
                blocked_comment.created_at = created_at
                blocked_comment.save()

    def test_comments_daily_breakdown(self):
        url = reverse("comments_daily_breakdown")
        date_from = (datetime.today().date() - timedelta(days=5)).strftime("%Y-%m-%d")
        date_to = datetime.today().date().strftime("%Y-%m-%d")
        response = self.client.get(url, {"date_from": date_from, "date_to": date_to})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]["blocked_comments"], 1)
        self.assertEqual(response.data[1]["blocked_comments"], 0)
        self.assertEqual(response.data[0]["total_comments"], 2)
        for entry in response.data:
            self.assertIn("date", entry)
            self.assertIn("total_comments", entry)
            self.assertIn("blocked_comments", entry)
