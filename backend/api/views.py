from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, ChatSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Chat

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

class ChatCreate(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class ChatDelete(generics.DestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(user=user)
    
    
# Dummy AI function – replace this with your actual chatbot logic or API call.
def generate_ai_response(conversation):
    # For example, simply echo the last message for now.
    last_user_msg = conversation[-1]["text"]
    return f"Echo: {last_user_msg}"

class ChatView(APIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request):
        # Fetch chats for the user; here we assume a logged-in user.
        chats = Chat.objects.filter(user=request.user)
        # Serialize chat objects appropriately
        serialized_chats = [
            {
                "id": chat.id,
                "title": chat.title,
                "messages": chat.content,  # Assumes this is a list of messages
                "send_at": chat.send_at,
            }
            for chat in chats
        ]
        return Response(serialized_chats, status=status.HTTP_200_OK)

    def post(self, request):
        title = request.data.get("title", "Untitled")
        messages = request.data.get("messages", [])

        # Save the chat. Ensure the user is authenticated.
        chat = Chat.objects.create(
            title=title, content=messages, user=request.user
        )

        # Assuming the last message is from the user, generate AI response.
        if messages and messages[-1]["sender"] == "user":
            ai_response_text = generate_ai_response(messages)
            ai_message = {"sender": "ai", "text": ai_response_text}
            messages.append(ai_message)
            # Update the chat with the new conversation
            chat.content = messages
            chat.save()

        return Response(
            {"id": chat.id, "title": chat.title, "messages": messages},
            status=status.HTTP_201_CREATED,
        )