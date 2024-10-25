# Django REST Framework Posts API with AI features

## Project overview
This project is a Django REST Framework API that provides functionalities for user authentication, managing posts and comments, content moderation, and analytics. It leverages JWT authentication for secure access, Celery for asynchronous tasks, and integrates with the Groq LLaMA AI model for content moderation and automatic response generation.

## Features

* User Registration and Authentication
  * JWT-based authentication using djangorestframework-simplejwt.
  * Registration endpoint returns JWT tokens upon successful signup.
* Posts Management
  * Create, retrieve, update, and delete posts.
  * Content moderation for posts using Groq LLaMA AI model.
  * Posts have statuses: pending, approved, blocked.
* Comments Management
  * Create, retrieve, update, and delete comments on posts.
  * Content moderation for comments.
  * Automatic responses to comments using Celery tasks and AI integration.
* Analytics
  * Endpoint to provide daily breakdown of comments.
  * Returns total comments and blocked comments per day within a date range.
* API Documentation
  * Interactive API documentation using drf-spectacular, Swagger UI
* Asynchronous Tasks
  * Celery integration for content moderation and automatic responses.
* AI Integration
  * Uses Groq LLaMA AI model for content moderation and response generation.

## Prerequisites

* Python 3.10+
* Redis (for Celery message broker)

## Installation

1. Clone the repository
```bash
git clone https://github.com/DmytroSliusarchuk/posts_ai_api.git
cd posts_ai_api
```

2. Create a virtual environment and activate it
```bash
python3 -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
```
Update the `.env` file with your settings.

5. Run migrations
```bash
python manage.py migrate
```

6. Start the Celery worker
```bash
celery -A posts_ai_api worker -l info
```

7. Start the Django development server
```bash
python manage.py runserver
```

## API Documentation

Access the interactive API documentation at:

- Swagger UI: http://localhost:8000/api/schema/swagger/

## Celery Tasks

The application uses Celery for asynchronous processing:

- Content Moderation: Posts and comments are moderated asynchronously using Celery tasks and the Groq LLaMA AI model.
- Automatic Responses: Automatic responses to comments are generated and moderated asynchronously.

## Content Moderation and Automatic Responses

- Content Moderation: When a post or comment is created, it is saved with a pending status and sent to a Celery task for moderation using the Groq LLaMA AI model. The status is updated to approved or blocked based on the moderation result.
- Automatic Responses: If enabled, the author of a post can have automatic responses generated for comments on their posts. These responses are generated and moderated asynchronously.


## Environment Variables

Ensure the following environment variables are set:

- SECRET_KEY: Your Django secret key.
- DEBUG: Set to True for development, False for production.
- GROQ_API_KEY: Your API key for the Groq LLaMA AI service.
- CELERY_BROKER_URL: URL for the Celery broker.

## Running Tests

Run the tests using the following command:

```bash
python manage.py test
```
