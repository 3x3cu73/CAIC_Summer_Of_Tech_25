import toast from "react-hot-toast";
import React, {useState} from "react";
import axios from 'axios';
import {useNavigate} from "react-router-dom";
const params = new URLSearchParams(window.location.search);
const apiBaseUrl = import.meta.env.VITE_API_BASE;


function ResetPassword() {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const resetToken = params.get('token');
    const resetMail = params.get('email');

    const [email, setEmail] = useState('');

    const emailHandler = (e: { target: { value: React.SetStateAction<string>; }; }) => {
        setEmail(e.target.value);
    }

    const [password, setPassword] = useState('');
    const passwordHandler = (e: { target: { value: React.SetStateAction<string>; }; }) => {
        setPassword(e.target.value);
    }

    const sendResetMail = () => {
        setLoading(true);

        axios.post(`${apiBaseUrl}/sendResetMail`, {email}, {
            headers: { 'Content-Type': 'application/json' },
            withCredentials: true,
        })
            .then((r) => {
                // toast.success(r.data.status);
                console.log(r.data);
                if (r.data.success){
                    toast.success(r.data.status);

                    navigate('/');
                }
                else {
                    toast.error(r.data.status);
                }
            })
            .catch((err) => {
                toast.error("Error"+' : '+err.response.data.error);
            }).finally(()=>{
            setLoading(false);
        })
    }


    const setNewPass = () => {
        setLoading(true);
        axios.post(`${apiBaseUrl}/resetPassword`, {newPassword : password, token : resetToken, email: resetMail}, {
            headers: { 'Content-Type': 'application/json' },
            withCredentials: true,
        }).then((r)=>{
            console.log(r.data);
            if (r.data.success){
                toast.success(r.data.status);
            }
            else {
                toast.error(r.data.status);
            }
        }).catch((err)=>{
            toast.error("Error"+' : '+err.response.data.error);
        }).finally(()=>{
            setLoading(false);
        });

    }

    return !resetToken?<>
        <h4>Enter email to get Password Reset link </h4>
    <input onChange={emailHandler} type="text" placeholder="Email"/>
    <button onClick={sendResetMail} disabled={loading}> {loading ? "Sending..." : "Send Mail"}</button>
    </>: <>
        <input type={"password"} placeholder={"<PASSWORD>"} onChange={passwordHandler}/>
        <button onClick={setNewPass} disabled={loading}>Reset Password</button>
    </>;
}

export default ResetPassword;
