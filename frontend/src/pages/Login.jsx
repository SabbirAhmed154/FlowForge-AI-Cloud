import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import api from "../api/api";


function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [message, setMessage] = useState("");


    const handleSubmit = async (e) => {

        e.preventDefault();

        setMessage("");

        const formData = new URLSearchParams();

        formData.append("username", username);

        formData.append("password", password);


        try {

            const response = await api.post(
                "/auth/login",
                formData,
                {
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    }
                }
            );


            localStorage.setItem(
                "access_token",
                response.data.access_token
            );


            navigate("/dashboard");

        } catch (error) {

            setMessage(
                error.response?.data?.detail
                || "Login failed"
            );
        }
    };


    return (

        <div className="auth-page">

            <div className="auth-card">

                <h1>FlowForge AI</h1>

                <h2>Login</h2>


                <form onSubmit={handleSubmit}>

                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={
                            (e) =>
                                setUsername(
                                    e.target.value
                                )
                        }
                        required
                    />


                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={
                            (e) =>
                                setPassword(
                                    e.target.value
                                )
                        }
                        required
                    />


                    <button type="submit">
                        Login
                    </button>

                </form>


                {message && (
                    <p className="error">
                        {message}
                    </p>
                )}


                <p>
                    Don't have an account?{" "}
                    <Link to="/register">
                        Register
                    </Link>
                </p>

            </div>

        </div>
    );
}


export default Login;