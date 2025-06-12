import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
    const navigate = useNavigate();

    useEffect(() => {
        const apiBaseUrl = import.meta.env.VITE_API_BASE;
        axios.post(`${apiBaseUrl}validate`, {}, {
            headers: { 'Content-Type': 'application/json' },
            withCredentials: true,
        })
            .then(() => setIsLoggedIn(true))
            .catch(() => setIsLoggedIn(false));
    }, []);

    useEffect(() => {
        if (isLoggedIn === false) {
            navigate('/login');
        }
    }, [isLoggedIn, navigate]);

    if (isLoggedIn === null) return <div>Loading...</div>;
    if (!isLoggedIn) return null;

    return <>Hi</>;
}

export default Dashboard;
