import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/api";


function Register() {

    const navigate = useNavigate();

    const [form, setForm] = useState({
        username: "",
        email: "",
        password: ""
    });

    const [message, setMessage] = useState("");


    const handleChange = (e) => {

        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    };


    const handleSubmit = async (e) => {

        e.preventDefault();

        setMessage("");

        try {

            await api.post(
                "/auth/register",
                form
            );

            navigate("/login");

        } catch (error) {

            setMessage(
                error.response?.data?.detail
                || "Registration failed"
            );
        }
    };


    return (

        <div className="auth-page">

            <div className="auth-card">

                <h1>FlowForge AI</h1>

                <h2>Create Account</h2>

                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        value={form.username}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={form.email}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={form.password}
                        onChange={handleChange}
                        required
                    />

                    <button type="submit">
                        Register
                    </button>

                </form>

                {message && (
                    <p className="error">
                        {message}
                    </p>
                )}

                <p>
                    Already have an account?{" "}
                    <Link to="/login">
                        Login
                    </Link>
                </p>

            </div>

        </div>
    );
}


export default Register;