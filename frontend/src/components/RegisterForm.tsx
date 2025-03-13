import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

import "../styles/Form.css";

interface FormProps {
  route: string;
  method: "doctor" | "patient";
}

function Form({ route, method }: FormProps) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  // const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    // setLoading(true);
    e.preventDefault();

    if (password != password2) {
      alert("Passwords must match!");
      return;
    }

    console.log(route);

    try {
      await api.post(route, {
        username: username,
        password: password,
        password2: password2,
      });
      navigate("/login");
    } catch (error) {
      alert(error);
    }
    // finally {
    // setLoading(false);
    // }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>Register as {method}</h1>
      <input
        className="form-input"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        className="form-input"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <input
        className="form-input"
        type="password"
        value={password2}
        onChange={(e) => setPassword2(e.target.value)}
        placeholder="Retype Password"
      />
      <button className="form-button" type="submit">
        Register as {method}
      </button>
    </form>
  );
}

export default Form;
