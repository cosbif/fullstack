import { useEffect, useState } from "react";
import { getImages } from "../api";
import { downloadImage, deleteImage } from "../api";

const API_URL = "http://127.0.0.1:8000";

function History() {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadImages() {
      try {
        const data = await getImages();
        setImages(data);
      } catch (err) {
        setError("Не удалось загрузить историю");
      } finally {
        setLoading(false);
      }
    }

    loadImages();
  }, []);

  if (loading) return <p className="loading">Загрузка<span>...</span></p>;
  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (images.length === 0) return <p>История пуста</p>;

  return (
    <div>
      <h1>История обработок</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
        gap: "20px",
        marginTop: "20px"
      }}>
        {images.map(img => (
          <div key={img.id} className="card">
            <p><strong>ID:</strong> {img.id}</p>
            <div style={{ display: "flex", gap: "10px", justifyContent: "center" }}>
              <img src={`${API_URL}/${img.original_path}`} width="140" />
              <img src={`${API_URL}/${img.processed_path}`} width="140" />
            </div>
            <div style={{ marginTop: "10px", display: "flex", gap: "10px", justifyContent: "center" }}>
              <button type="button" onClick={() => downloadImage(img.id)}>Скачать</button>
              <button type="button" onClick={async () => {
                try {
                  await deleteImage(img.id);
                  setImages(images.filter(i => i.id !== img.id));
                } catch (err) {
                  alert("Ошибка при удалении");
                } 
              }}>Удалить</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;
