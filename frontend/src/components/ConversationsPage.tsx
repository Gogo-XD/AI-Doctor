import { useState, useEffect } from "react";
import api from "../api";

interface Conversation {
  id: number;
  conversation_type: string;
}

interface Message {
  id: number;
  sender: string;
  text: string;
}

function ConversationsPage({ refreshFlag }: { refreshFlag: boolean }) {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState<
    number | null
  >(null);
  const [messages, setMessages] = useState([]);
  const [currMessage, setCurrMessage] = useState("");
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);

  async function fetchConversations() {
    try {
      const res = await api.get("/api/messaging/conversations/");
      setConversations(res.data);
    } catch (error) {
      console.error("Error fetching conversations", error);
    } finally {
      setLoadingConversations(false);
    }
  }

  useEffect(() => {
    fetchConversations();
  }, [refreshFlag]);

  // Fetch messages when a conversation is selected
  useEffect(() => {
    async function fetchMessages() {
      if (!selectedConversation) return;
      setLoadingMessages(true);
      try {
        const res = await api.get("/api/messaging/messages/", {
          params: { conversation: selectedConversation },
        });
        setMessages(res.data);
      } catch (error) {
        console.error("Error fetching messages", error);
      } finally {
        setLoadingMessages(false);
      }
    }
    fetchMessages();
  }, [selectedConversation]);

  const sendMessage = async () => {
    if (!selectedConversation || !currMessage.trim()) return;
    try {
      await api
        .post("/api/messaging/create-message/", {
          conversation: selectedConversation,
          text: currMessage,
        })
        .then(() => setCurrMessage(""));
      const res = await api.get("/api/messaging/messages/", {
        params: { conversation: selectedConversation },
      });
      setMessages(res.data);
    } catch (error) {
      console.error("Error sending message", error);
    }
  };

  const deleteConversation = async () => {
    if (!selectedConversation) return;
    try {
      await api.delete("/api/messaging/delete-conversation/", {
        params: { conversation: selectedConversation },
      });
      fetchConversations();
      setSelectedConversation(null);
    } catch (error) {
      console.error("Error deleting", error);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left Sidebar: Conversation List */}
      <div
        style={{
          width: "250px",
          borderRight: "1px solid #ccc",
          padding: "10px",
        }}
      >
        <h2>Conversations</h2>
        {loadingConversations ? (
          <p>Loading...</p>
        ) : (
          conversations.map((conv: Conversation) => (
            <button
              key={conv.id}
              onClick={() => setSelectedConversation(conv.id)}
              style={{
                display: "block",
                width: "100%",
                marginBottom: "10px",
                backgroundColor:
                  conv.id === selectedConversation ? "#ddd" : "#fff",
                border: "1px solid #ccc",
                padding: "8px",
                textAlign: "left",
              }}
            >
              Conversation {conv.id} ({conv.conversation_type})
            </button>
          ))
        )}
      </div>

      {/* Right Pane: Conversation Detail */}
      <div style={{ flex: 1, padding: "10px" }}>
        {selectedConversation ? (
          loadingMessages ? (
            <p>Loading messages...</p>
          ) : (
            <>
              <h2>Conversation {selectedConversation}</h2>
              <div style={{ marginBottom: "20px" }}>
                {messages.map((msg: Message) => (
                  <div key={msg.id} style={{ marginBottom: "10px" }}>
                    <strong>{msg.sender}:</strong> {msg.text}
                  </div>
                ))}
              </div>
              <input
                type="text"
                placeholder="Type your message..."
                value={currMessage}
                onChange={(e) => setCurrMessage(e.target.value)}
                style={{ width: "80%", padding: "8px" }}
              />
              <button
                onClick={sendMessage}
                style={{ padding: "8px", marginLeft: "10px" }}
              >
                Send
              </button>
            </>
          )
        ) : (
          <p>Please select a conversation.</p>
        )}

        <button onClick={deleteConversation}>Delete Conversation</button>
      </div>
    </div>
  );
}

export default ConversationsPage;
