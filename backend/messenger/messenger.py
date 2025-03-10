from .input import Audio, Text

class Messenger:
    def __init__(self):
        self.audio_manager = Audio()
        self.text_manager = Text()
        self.history = []
        self.messages = []
        self.client = None

    def start(self, client):
        self.client = client
        with open("messenger/system_message.txt", "r") as f:
            self.system_message = {"role": "system", "content": f.read()}
        self.messages.append(self.system_message)

    def audio_message(self, audio_file_path):
        self.audio_manager.client = self.client
        transcription = self.audio_manager.process_audio_file(audio_file_path)
        return self.send()

    def text_message(self, user_text):
        self.text_manager.run(user_text)
        return self.send()

    def retrieve_text(self):
        with open("output.txt", "r") as f:
            text = f.read()
        self.messages.append({"role": "user", "content": text})

    def send(self):
        self.retrieve_text()
        response_stream = self.client.chat.completions.create(
            messages=self.messages,
            model="llama3-70b-8192",
            temperature=0.5,
            stream=True
        )
        return_text = ""
        for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content is not None:
                return_text += content
                print(content, end="")
        self.history.extend(self.messages)
        self.messages.clear()
        return return_text
