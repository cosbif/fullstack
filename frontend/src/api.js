const API_URL = "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("token");
}

async function request(path, options = {}) {
  const headers = options.headers || {};

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  headers["Content-Type"] = "application/json";

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "API error");
  }

  return response.json();
}

/* =========================
   AUTH
========================= */

export function login(email, password) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function register(email, password) {
  return request("/users/", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function getMe() {
  return request("/users/me");
}

/* =========================
   IMAGES
========================= */

export function getImages() {
  return request("/images/");
}

export function addImage(data) {
  return request("/images/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function uploadImage(file) {
  const token = localStorage.getItem("token");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/images/upload", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }

  return response.json();
}

export async function downloadImage(imageId) {
  const token = localStorage.getItem("token");
  const response = await fetch(`http://127.0.0.1:8000/images/download/${imageId}`, {
    method: "GET",
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
    },
  });

  if (!response.ok) throw new Error("Ошибка скачивания");

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `image_${imageId}.png`;
  document.body.appendChild(a);
  a.click();
  a.remove();
}

export async function deleteImage(imageId) {
  const token = localStorage.getItem("token");
  const response = await fetch(`http://127.0.0.1:8000/images/${imageId}`, {
    method: "DELETE",
    headers: {
      Authorization: token ? `Bearer ${token}` : "",
    },
  });
  if (!response.ok) throw new Error("Ошибка удаления");
}
