from celery import shared_task

from .models import Post, Comment, Statuses
from .utils import moderate_content, generate_response_content


@shared_task
def moderate_post_content(post_id):
    """
    Task to moderate the content of a post.
    """

    try:
        post = Post.objects.get(id=post_id)
        is_acceptable = moderate_content(post.content)
        if is_acceptable:
            post.status = Statuses.APPROVED
        else:
            post.status = Statuses.BLOCKED
        post.save()
    except Exception as e:
        print("Error moderating post content: ", e)


@shared_task
def moderate_comment_content(comment_id):
    """
    Task to moderate the content of a comment.
    """

    try:
        comment = Comment.objects.get(id=comment_id)
        is_acceptable = moderate_content(comment.content)
        if is_acceptable:
            comment.status = Statuses.APPROVED
            comment.save()

            post = comment.post
            if post.author.auto_response_enabled and post.author != comment.author:
                delay = post.author.auto_response_delay
                generate_auto_response.apply_async(
                    args=[comment.id], countdown=delay * 60
                )
        else:
            comment.status = Statuses.BLOCKED
            comment.save()
    except Exception as e:
        print("Error moderating comment content: ", e)


@shared_task
def generate_auto_response(comment_id):
    """
    Task to generate an automatic response to a comment.
    """

    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.status != Statuses.APPROVED:
            return
        post = comment.post
        author = post.author

        response_content = generate_response_content(post.content, comment.content)

        Comment.objects.create(
            post=post, author=author, content=response_content, status=Statuses.APPROVED
        )
    except Exception as e:
        print("Error generating auto response: ", e)
