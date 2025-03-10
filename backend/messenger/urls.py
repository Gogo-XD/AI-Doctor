# urls.py
from django.urls import path
from .views import MessengerView

urlpatterns = [
    path("", MessengerView.as_view(), name="messenger"),
]
