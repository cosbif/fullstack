import { useState } from "react";
import { uploadImage } from "../api";

const API_URL = "http://127.0.0.1:8000";

function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const data = await uploadImage(file);
      setResult(data);
      setError("");
    } catch {
      setError("Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Загрузка изображения</h1>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload}>Загрузить и анонимизировать</button>

      {loading && <p className="loading">Загрузка<span>...</span></p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ display: "flex", gap: "20px", justifyContent: "center", marginTop: "20px" }}>
          <div className="card">
            <p>Оригинал</p>
            <img src={`${API_URL}/${result.original_path}`} width="300" />
          </div>
          <div className="card">
            <p>Анонимизировано</p>
            <img src={`${API_URL}/${result.processed_path}`} width="300" />
          </div>
        </div>
      )}
    </div>
  );
}

export default Upload;