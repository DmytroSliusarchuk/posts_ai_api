from django.conf import settings
from groq import Groq


client = Groq(
    api_key=settings.GROQ_API_KEY,
)
