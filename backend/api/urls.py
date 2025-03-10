from django.urls import path, include
from .views import ChatView


urlpatterns = [
    path("chats/", ChatView.as_view(), name="chats"),
    path("messenger/", include('messenger.urls'))
    # Add other endpoints (like delete) as needed.
]