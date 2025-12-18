import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      await register(email, password);
      navigate("/login");
    } catch (err) {
      alert("Ошибка регистрации");
    }
  };

  return (
    <div>
      <h1>Регистрация</h1>

      <input
        type="email"
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      /><br/>

      <input
        type="password"
        placeholder="Пароль"
        onChange={(e) => setPassword(e.target.value)}
      /><br/>

      <button onClick={handleSignup}>Зарегистрироваться</button>
    </div>
  );
}

export default Signup;
