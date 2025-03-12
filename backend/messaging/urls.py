from django.urls import path
from .views import CreateConversationView, CreateMessageView, ListConversationView, ListMessagesView, DeleteConversationView

urlpatterns = [
    path('create-conversation/', CreateConversationView.as_view(), name='create-conversation'),
    path('delete-conversation/', DeleteConversationView.as_view(), name='delete-conversation'),
    path('conversations/', ListConversationView.as_view(), name='list-conversation'),
    path('create-message/', CreateMessageView.as_view(), name='create-message'),
    path('messages/', ListMessagesView.as_view(), name='list-message'),
]
