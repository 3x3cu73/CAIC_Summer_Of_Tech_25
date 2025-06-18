import './App.css'
import { Routes, Route } from 'react-router-dom';
import Register from "./components/login/register.tsx";
import Login from "./components/login/login.tsx";
import Dashboard from "./components/dashboard/dashboard.tsx";
import {Toaster} from "react-hot-toast";
import ResetPassword from "./components/login/passReset.tsx";

function App() {

    return (
        <>
            <Toaster position="top-center" reverseOrder={false} />

            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/reset-password" element={<ResetPassword />}/>
            </Routes>
        </>
    );

}

export default App
