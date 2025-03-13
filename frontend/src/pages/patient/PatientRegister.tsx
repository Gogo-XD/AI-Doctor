import RegisterForm from "../../components/RegisterForm";

function RegisterPatient() {
  return (
    <>
      <RegisterForm
        route="/api/user/register/register-patient/"
        method="patient"
      ></RegisterForm>
    </>
  );
}

export default RegisterPatient;
