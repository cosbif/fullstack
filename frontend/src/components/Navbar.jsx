import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function Navbar() {
  const isAuth = useAuth();
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const style = {
    display: "flex",
    gap: "20px",
    padding: "15px 30px",
    borderBottom: "1px solid #333",
    backgroundColor: "#1a1a1a",
    alignItems: "center",
    justifyContent: "space-between",
    position: "sticky",
    top: 0,
    zIndex: 100,
  };

  return (
    <nav style={style}>
      <Link to="/">Главная</Link>

      {isAuth && (
        <>
          <Link to="/upload">Загрузить фото</Link>
          <Link to="/history">История</Link>
          <button onClick={logout}>Выйти</button>
        </>
      )}

      {!isAuth && (
        <>
          <Link to="/login">Войти</Link>
          <Link to="/signup">Регистрация</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;
