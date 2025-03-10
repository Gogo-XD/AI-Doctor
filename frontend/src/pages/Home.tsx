import React, { useState } from "react";
import api from "../api";

function Home() {
  const [inputType, setInputType] = useState("text"); // "text" or "audio"
  const [textInput, setTextInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputType === "text") {
      try {
        const res = await api.post("/api/messenger/", {
          input_type: "text",
          text: textInput,
        });
        setResponse(res.data.response);
      } catch (error) {
        alert("Error sending text: " + error);
      }
    }
  };

  return (
    <div>
      <div>
        <button onClick={() => setInputType("text")}>Text Input</button>
        <button onClick={() => setInputType("audio")}>Audio Input</button>
      </div>

      {inputType === "text" && (
        <form onSubmit={handleSend}>
          <input
            type="text"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Type your message..."
          />
          <button type="submit">Send</button>
        </form>
      )}

      {inputType === "audio" && (
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const fileInput = document.getElementById(
              "audioInput"
            ) as HTMLInputElement;
            if (fileInput && fileInput.files && fileInput.files.length > 0) {
              const formData = new FormData();
              formData.append("input_type", "audio");
              formData.append("audio", fileInput.files[0]);
              try {
                const res = await api.post("/api/messenger/", formData, {
                  headers: { "Content-Type": "multipart/form-data" },
                });
                setResponse(res.data.response);
              } catch (error) {
                alert("Error sending audio: " + error);
              }
            }
          }}
        >
          <input id="audioInput" type="file" accept="audio/*" />
          <button type="submit">Send Audio</button>
        </form>
      )}

      <div className="chatbox">
        <h3>Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default Home;
