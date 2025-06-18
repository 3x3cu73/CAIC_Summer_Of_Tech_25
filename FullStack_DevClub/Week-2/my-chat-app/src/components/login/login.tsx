import React, {useState} from "react";
import axios from 'axios';
import {Link, useNavigate} from "react-router-dom";
import toast from "react-hot-toast";

type Props = {
    children?: React.ReactNode,
};

const apiBaseUrl = import.meta.env.VITE_API_BASE;

function Login({children}: Props) {
    const navigate = useNavigate();
    // 1. State variables for username and password
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    // 2. Handler for username input changes
    const handleUsernameChange = (e: any) => {
        setUsername(e.target.value);
    };

    // 3. Handler for password input changes
    const handlePasswordChange = (e: any) => {
        setPassword(e.target.value);
    };

    // 4. Handler for form submission
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();


        axios.post(
            `${apiBaseUrl}/login`,
            {username, password},
            {
                headers: {'Content-Type': 'application/json'},
                withCredentials: true,
            }
        )
            .then(res => {
                toast.success('Login successful');
                console.log('Login successful:', res.data);
                navigate('/');

            })
            .catch(err => {toast.error('Login failed ', err.response ? err.response.data['error'] : err.message);
                console.error('Login failed:', err.response ? err.response.data : err.message);
            });

    };

    return (
        <div
            className="bg-gradient-to-br from-indigo-500 to-purple-600 min-h-screen flex items-center justify-center p-4">
            <div
                className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 hover:scale-[1.02] hover:shadow-3xl">
                <h2 className="text-4xl font-extrabold text-center text-gray-900 mb-8">
                    Welcome Back!
                </h2>


                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="username"
                               className="block text-sm font-medium text-gray-700 sr-only">Username</label>
                        <input
                            type="text"
                            name="username"
                            id="username"
                            placeholder="Username"
                            className="block w-full px-4 py-3 border border-gray-300 rounded-lg text-lg placeholder-gray-500 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
                            value={username}
                            onChange={handleUsernameChange}
                            required
                        />
                    </div>

                    <div>
                        <label htmlFor="password"
                               className="block text-sm font-medium text-gray-700 sr-only">Password</label>
                        <input
                            type="password"
                            name="password"
                            id="password"
                            placeholder="Password"
                            className="block w-full px-4 py-3 border border-gray-300 rounded-lg text-lg placeholder-gray-500 focus:ring-blue-500 focus:border-blue-500 transition duration-150 ease-in-out"
                            value={password}
                            onChange={handlePasswordChange}
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75 transition duration-150 ease-in-out shadow-lg hover:shadow-xl"
                    >
                        Login
                    </button>
                </form>

                <div className="mt-8 text-center text-gray-600 text-sm">
                    Don't have an account?
                    <Link to="/register"
                       className="font-medium text-blue-600 hover:text-blue-700 transition duration-150 ease-in-out ml-1">Sign
                        Up</Link>
                </div>
                <div className="mt-2 text-center text-gray-600 text-sm">
                    <Link to="/reset-password"
                       className="font-medium text-blue-600 hover:text-blue-700 transition duration-150 ease-in-out">Forgot
                        Password?</Link>
                </div>
            </div>

            {children && (
                <div className="mt-8 text-white text-center">
                    {children}
                </div>
            )}
        </div>
    );
}

export default Login;
