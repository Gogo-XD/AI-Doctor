import os
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .messenger import Messenger
from groq import Groq

client = Groq(api_key="...")

# Create a Messenger instance.
messenger = Messenger()
messenger.start(client)

# Set up the Groq client as needed and start the messenger.
# For example:
# from your_groq_module import groq_client
# messenger.start(groq_client)

class MessengerView(APIView):
    def post(self, request):
        input_type = request.data.get("input_type")
        if input_type == "text":
            user_text = request.data.get("text", "")
            if not user_text.strip():
                return Response(
                    {"error": "Empty text input."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Call text_message and pass the user input directly.
            response_text = messenger.text_message(user_text)
            return Response({"response": response_text}, status=status.HTTP_200_OK)

        elif input_type == "audio":
            audio_file = request.FILES.get("audio")
            if not audio_file:
                return Response(
                    {"error": "No audio file provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Process the uploaded audio file.
            transcription = messenger.audio_manager.process_audio_file(tmp_path)
            os.remove(tmp_path)
            # Get the AI response after processing the transcription.
            response_text = messenger.send()
            return Response(
                {"response": response_text, "transcription": transcription},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"error": "Invalid input type. Must be 'text' or 'audio'."},
                status=status.HTTP_400_BAD_REQUEST
            )
