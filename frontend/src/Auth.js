import { useState } from "react";
import { signup, signin, updateUser, deleteUser } from "./api";

export default function Auth() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [token, setToken] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  return (
    <div>
      <h2>Auth</h2>
      <input name="username" placeholder="Username" onChange={handleChange} />
      <input name="password" type="password" onChange={handleChange} />

      <button onClick={() => signup(form)}>Signup</button>

      <button
        onClick={async () => {
          const res = await signin(form);
          setToken(res.access_token);
        }}
      >
        Signin
      </button>

      <button onClick={() => updateUser("newpassword", token)}>
        Update Password
      </button>

      <button onClick={() => deleteUser(token)}>Delete Account</button>
    </div>
  );
}
