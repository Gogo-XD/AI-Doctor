from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')

class Messenger:
  def __init__(self):
    self.client = OpenAI (
      base_url="https://api.cohere.ai/compatibility/v1",
      api_key = API_KEY
    )

  def send(self, text, history):
    ai_text = ""
    messages = []
    messages.append(self.retrieve_system_text())
    messages.extend(self.retrieve_history(history))
    messages.append(self.retrieve_text(text))

    stream = self.client.chat.completions.create(
    model="command-r7b-12-2024",
    messages=messages,
    stream=True,
    )
    for chunk in stream:
        ai_text += chunk.choices[0].delta.content or ""
        print(chunk.choices[0].delta.content or "", end="")

    return ai_text


  def retrieve_system_text(self):
    f = open("system_message.txt", "r")
    content = f.read()
    f.close
    return {"role": "system", "content": content}


  def retrieve_history(self, history):
    return history
    
     
  def retrieve_text(self, text):
    return {"role": "user", "content": text}

  