from django.urls import path
from app.shortener.views import URLApiView, ShortURLRedirectView

urlpatterns = [
    path('api/v1/link', URLApiView.as_view()),
    path('<slug:slug>', ShortURLRedirectView.as_view()),
]
