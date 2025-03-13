import RegisterForm from "../../components/RegisterForm";

function RegisterDoctor() {
  return (
    <>
      <RegisterForm
        route="/api/user/register/register-doctor/"
        method="doctor"
      ></RegisterForm>
    </>
  );
}

export default RegisterDoctor;
