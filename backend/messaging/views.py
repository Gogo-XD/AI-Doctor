from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .messenger import Messenger

class CreateConversationView(generics.CreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class CreateMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation does not exist.")

        if conversation.conversation_type == 'ai':
            if conversation.patient != self.request.user:
                raise serializers.ValidationError("You are not allowed to post in this conversation.")
            user_message = serializer.save(conversation=conversation, sender="user")

            history = Message.objects.filter(
                conversation__id=conversation_id,
                conversation__patient=self.request.user
            ).order_by("date")

            formatted_history = [
                {"role": "assistant", "content": msg.text} for msg in history
            ]

            # Initialize Messenger here
            messenger = Messenger()
            ai_text = messenger.send(user_message.text, formatted_history)
            Message.objects.create(conversation=conversation, sender="ai", text=ai_text)

        elif conversation.conversation_type == 'doctor':
            if conversation.patient != self.request.user and not self.request.user.groups.filter(name='Doctor').exists():
                raise serializers.ValidationError("You are not allowed to post in this conversation.")
            sender = "doctor" if self.request.user.groups.filter(name='Doctor').exists() else "user"
            serializer.save(conversation=conversation, sender=sender)
        else:
            raise serializers.ValidationError("Invalid conversation type.")


class ListConversationView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(patient=self.request.user)


class ListMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        return Message.objects.filter(
            conversation__id=conversation_id,
            conversation__patient=self.request.user
        ).order_by("date")
    

class DeleteConversationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the conversation id from the query parameters
        conversation_id = self.request.query_params.get("conversation")
        if not conversation_id:
            raise serializers.ValidationError("Conversation id not provided.")
        try:
            # Manually get the conversation ensuring it belongs to the logged-in user
            conversation = Conversation.objects.get(id=conversation_id, patient=self.request.user)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation not found.")
        return conversation

    def delete(self, request, *args, **kwargs):
        conversation = self.get_object()
        # Delete the conversation using the model's delete() method directly
        conversation.delete()
        return Response(status=204)

