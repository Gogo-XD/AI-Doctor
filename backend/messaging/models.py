from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CONVERSATION_TYPES = (
    ('ai', 'User-AI Conversation'),
    ('doctor', 'User-Doctor Conversation'),
)

class Conversation(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default='ai')
    started_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active')
    
    def __str__(self):
        return f"Conversation {self.id} ({self.conversation_type}) with {self.patient.username}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in Conversation {self.conversation.id}"