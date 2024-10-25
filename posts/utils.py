from posts_ai_api.ai_client import client


def moderate_content(content):
    """
    Function to moderate content using the GROQ API.
    """

    prompt = (
        f"Validate the following content: '{content}' "
        f"If it contains obscene words, hate speech, or any other inappropriate content, return 0. "
        f"Otherwise, return 1. Don't return any other except 0 or 1. "
        f"Don't provide any explanation and extra information."
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        top_p=0,
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    if "0" in response:
        return False
    return True


def generate_response_content(post_content, comment_content):
    """
    Function to generate a response to a user comment on a post.
    """

    prompt = (
        f"You are the author of a post with the following content: '{post_content}'. "
        f"A user has commented on your post with the following content: '{comment_content}'. "
        f"Generate a response to the user comment. The response should be polite, respectful, and engaging. "
        f"Try to encourage further discussion or provide additional information related to the post content."
        f"Please provide a response to the user comment without any additional information or explanation."
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1,
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    return response
