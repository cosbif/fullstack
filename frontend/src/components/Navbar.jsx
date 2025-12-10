import { Link } from "react-router-dom";

function Navbar() {
  const style = {
    display: "flex",
    gap: "20px",
    padding: "10px",
    borderBottom: "1px solid #ccc",
  };

  return (
    <nav style={style}>
      <Link to="/">Главная</Link>
      <Link to="/upload">Загрузить фото</Link>
      <Link to="/history">История</Link>
      <Link to="/login">Войти</Link>
      <Link to="/signup">Регистрация</Link>
    </nav>
  );
}

export default Navbar;
