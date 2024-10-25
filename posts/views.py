from django.db.models.functions import TruncDate
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Post, Comment, Statuses
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .tasks import moderate_post_content, moderate_comment_content


@extend_schema(
    description="Retrieve a list of posts or create a new post.",
    responses={200: PostSerializer(many=True)},
)
class PostListCreateView(generics.ListCreateAPIView):
    """
    View to retrieve a list of posts or create a new post.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.filter(status=Statuses.APPROVED)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user, status=Statuses.PENDING)
        moderate_post_content.delay(post.id)


@extend_schema(
    description="Retrieve, update, or delete a specific post.",
    responses={200: PostSerializer},
)
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific post.
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Post.objects.filter(status=Statuses.APPROVED)


class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to retrieve a list of comments for a post or create a new comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        description="Retrieve a list of comments for a post or create a new comment.",
        responses={200: CommentSerializer(many=True)},
    )
    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id, status=Statuses.APPROVED)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs["post_id"])
        if post.status != Statuses.APPROVED:
            raise ValidationError("You can't comment on a post that is not approved.")

        comment = serializer.save(
            author=self.request.user, post=post, status=Statuses.PENDING
        )

        moderate_comment_content.delay(comment.id)


@extend_schema(
    description="Retrieve, update, or delete a specific comment.",
    responses={200: CommentSerializer},
)
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific comment.
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Comment.objects.filter(status=Statuses.APPROVED)


class CommentsDailyBreakdownView(APIView):
    """
    View to retrieve daily breakdown of comments within a date range.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Retrieve daily breakdown of comments within a date range.",
        parameters=[
            OpenApiParameter(
                "date_from",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description="Start date in YYYY-MM-DD format.",
                required=True,
            ),
            OpenApiParameter(
                "date_to",
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description="End date in YYYY-MM-DD format.",
                required=True,
            ),
        ],
        responses={200: OpenApiTypes.OBJECT},
    )
    def get(self, request):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if not date_from or not date_to:
            return Response(
                {"error": "date_from and date_to parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            date_from_parsed = parse_date(date_from)
            date_to_parsed = parse_date(date_to)
            if date_from_parsed is None or date_to_parsed is None:
                raise ValueError
            if date_from_parsed > date_to_parsed:
                return Response(
                    {"error": "date_from must be earlier than or equal to date_to."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comments = Comment.objects.filter(
            created_at__date__gte=date_from_parsed,
            created_at__date__lte=date_to_parsed,
        )

        daily_stats = (
            comments.annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(
                total_comments=Count("id"),
                blocked_comments=Count("id", filter=Q(status=Statuses.BLOCKED)),
            )
            .order_by("date")
        )

        result = []
        for entry in daily_stats:
            result.append(
                {
                    "date": entry["date"],
                    "total_comments": entry["total_comments"],
                    "blocked_comments": entry["blocked_comments"],
                }
            )

        return Response(result, status=status.HTTP_200_OK)
