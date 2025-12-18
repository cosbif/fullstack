import { useEffect, useState } from "react";
import { getMe } from "../api";

function Dashboard() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadUser() {
      try {
        const data = await getMe();
        setUser(data);
      } catch (err) {
        setError("Не удалось загрузить данные пользователя");
      }
    }

    loadUser();
  }, []);

  if (error) {
    return <p>{error}</p>;
  }

  if (!user) {
    return <p>Загрузка...</p>;
  }

  return (
    <div>
      <h1>Личный кабинет</h1>
      <p>Email: {user.email}</p>
      <p>ID пользователя: {user.id}</p>
    </div>
  );
}

export default Dashboard;
