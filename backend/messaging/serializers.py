from rest_framework import serializers
from .models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'patient', 'conversation_type', 'started_at', 'status']
        read_only_fields = ['id', 'patient', 'started_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'date']
        read_only_fields = ['id', 'date', 'sender']