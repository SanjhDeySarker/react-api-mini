const API = "http://localhost:8000";

export const signup = (data) =>
  fetch(`${API}/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

export const signin = async (data) => {
  const res = await fetch(`${API}/signin`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const updateUser = (password, token) =>
  fetch(`${API}/user`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ password }),
  });

export const deleteUser = (token) =>
  fetch(`${API}/user`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
