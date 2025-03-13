import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  const handleDoctorButton = () => {
    navigate("/register/register-doctor");
  };

  const handlePatientButton = () => {
    navigate("/register/register-patient");
  };

  return (
    <>
      <button onClick={handleDoctorButton}>Doctor</button>
      <button onClick={handlePatientButton}>Patient</button>
    </>
  );
}

export default Register;
