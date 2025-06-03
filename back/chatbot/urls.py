from django.urls import path
from .views import ai_chatbot_view

urlpatterns = [
    path("ai/", ai_chatbot_view, name="ai-chatbot"),
]
