import os
import tempfile
import wave

class Audio:
    def __init__(self):
        self.sample_rate = 16000
        self.channels = 1
        self.chunk = 1024

    def output_reset(self):
        with open("output.txt", "w") as f:
            f.write("")

    def output(self, text):
        with open("output.txt", "a") as f:
            f.write(text)

    def transcribe_audio(self, audio_file_path):
        try:
            with open(audio_file_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(audio_file_path), file.read()),
                    model="whisper-large-v3",
                    prompt=(
                        "The audio is by a patient to a doctor. The patient is describing "
                        "their symptoms and the doctor is providing a diagnosis"
                    ),
                    response_format="text",
                    language="en",
                )
            return transcription  
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def process_audio_file(self, audio_file_path):
        # Process the provided file instead of recording live
        self.output_reset()
        transcription = self.transcribe_audio(audio_file_path)
        self.output(transcription)
        return transcription


class Text:
    def run(self, text):
        self.output(text)

    def output(self, text):
        with open("output.txt", "w") as f:
            f.write(text)
