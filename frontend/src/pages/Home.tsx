import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import DoctorHome from "./doctor/DoctorHome";
import PatientHome from "./patient/PatientHome";

function Home() {
  const [homepage, setHomepage] = useState("");
  const navigate = useNavigate();

  const getHomePage = async () => {
    const res = await api.get("api/user/profile/");
    setHomepage(res.data.role);
  };

  useEffect(() => {
    getHomePage();
  });

  if (homepage === "doctor") {
    return <DoctorHome />;
  } else if (homepage === "patient") {
    return <PatientHome />;
  } else if (homepage === "unknown") {
    alert("Unrecognized Account");
    navigate("/login");
  }
}
export default Home;
