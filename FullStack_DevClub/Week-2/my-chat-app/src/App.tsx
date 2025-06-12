import './App.css'
import { Routes, Route } from 'react-router-dom';
import Register from "./components/login/register.tsx";
import Login from "./components/login/login.tsx";
import Dashboard from "./components/dashboard/dashboard.tsx";
import {Toaster} from "react-hot-toast";
function App() {

    return (
        <>
            <Toaster position="top-right" reverseOrder={false} />

            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </>
    );

}

export default App
