import { useState } from "react";
import api from "../../api";
import ConversationsPage from "../../components/ConversationsPage";

function PatientHome() {
  const [refreshFlag, setRefreshFlag] = useState(false);

  const newDoctorConversation = async () => {
    try {
      await api.post("api/messaging/create-conversation/", {
        conversation_type: "doctor",
        status: "active",
      });
      setRefreshFlag((prev) => !prev);
    } catch (error) {
      console.log(error);
    }
  };

  const newAIConversation = async () => {
    try {
      await api.post("api/messaging/create-conversation/", {
        conversation_type: "ai",
        status: "active",
      });
      setRefreshFlag((prev) => !prev);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <button onClick={newDoctorConversation}>
        Create Doctor Conversation
      </button>
      <button onClick={newAIConversation}>Create AI Conversation</button>
      <ConversationsPage refreshFlag={refreshFlag} />
    </>
  );
}
export default PatientHome;
