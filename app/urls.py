from django.urls import path
from app.shortener.views import URLApiView

urlpatterns = [
    path('api/v1/link', URLApiView.as_view()),
]
