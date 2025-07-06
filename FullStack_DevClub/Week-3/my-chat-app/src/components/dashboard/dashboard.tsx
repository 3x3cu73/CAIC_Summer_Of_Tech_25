import {useEffect, useState} from "react";
import {LogOut, Plus} from 'lucide-react';
import axios from 'axios';
import {useNavigate} from "react-router-dom";
import toast from "react-hot-toast";
import Chat from "../chats/chat.tsx";
import MessageArea from "../chats/messageArea.tsx";
import Modal from "../modal/modal.tsx";
import AddUser from "../chats/addUser.tsx";
import {useUser} from "../../context/userContext.tsx";

const apiBaseUrl = import.meta.env.VITE_API_BASE;

function Dashboard() {

    const {user,loading} = useUser();


    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [currChat, setCurrChat] = useState<any>('');
    const [chats, setChats] = useState<any[]>([]);
    const [Messages, setMessages] = useState<any[]>([]);


    //Modal Controller for Add New Chats
    const [chatUsers, setChatUsers] = useState<any[]>([]);
    const [allUsers, setAllUsers] = useState<any[]>([]);
    const [newChatName, setNewChatName] = useState<string>('');

    const [isChatModalOpen, setIsChatModalOpen] = useState(false);
    const handleCloseChatModal = () => {
        setIsChatModalOpen(false);
    };
    const handleOpenChatModal = () => {
        setIsChatModalOpen(true);
        getAllUsers();
        // console.log("All Users", allUsers);
    };

    const addChat = (selectedUser: any) => {

        const exists = chatUsers.some(u => u._id === selectedUser._id);

        if (exists) {
            setChatUsers(chatUsers.filter(u => u._id !== selectedUser._id));
        } else {
            setChatUsers([...chatUsers, selectedUser]);
        }

        //
        // console.log(chatUsers, "Current User", selectedUser);
    };

    useEffect(() => {
        if (!loading && user?._id) {
            setChatUsers([user]);
        }
    }, [loading, user]);


    const createChat = () => {
        // setChatUsers([...chatUsers, user?._id]);
        // console.log("createChat", chatUsers, newChatName);
        axios.post(`${apiBaseUrl}/chat/newChat`, {
            name : newChatName,
            participants : chatUsers.map(user => user._id),

        },{
            headers: {'Content-Type': 'application/json'},
            withCredentials: true,
        }).then(res => {
            // console.log(res , "Response is here");
            toast.success(res.data.message);
            setIsChatModalOpen(false);
        }).catch(err => {
            console.log(err);
            toast.error(err.response.data.message);
        })
    };



    const LucidClass = "cursor-pointer color-gray-600 hover:text-blue-400";
    const navigate = useNavigate();
    useEffect(() => {
        axios.post(`${apiBaseUrl}/auth/validate`, {}, {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true
        }).then(() => {

            if (!isLoggedIn) {
                toast.success('You are logged in');
                setIsLoggedIn(true);
            }

        }).catch((error) => {
            if (isLoggedIn) {
                toast.error('You are not logged in :', error.response ? error.response.data['error'] : error.message);
                setIsLoggedIn(false);
            }

            navigate('/login');
        });
    }, [isLoggedIn]);


    useEffect(() => {
        axios.post(`${apiBaseUrl}/chat/getChats`, {}, {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true
        }).then((response) => {
            // console.log('Chats:', response.data);

            setCurrChat(response.data[0]);
            setChats(response.data);

        }).catch((error) => {
            console.error('Error:', error.response ? error.response.data : error.message);
        });
    }, []);


    useEffect(() => {
        if (currChat){
            axios.post(`${apiBaseUrl}/chat/getMessages`, {
                chat: currChat._id,
            }, {
                headers: {'Content-Type': 'application/json'},
                withCredentials: true
            }).then((response) => {
                // console.log('Messages:', response.data,currChat._id);
                setMessages(response.data);


            })
    }

    }, [currChat]);

    // console.log('Current chat:', currChat);

    function logOut() {
        axios.post(`${apiBaseUrl}/auth/logout`, {}, {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true
        }).then(() => {
            setIsLoggedIn(false);
            // navigate('/login');
            toast.success('You are logged out');
        }).catch((error) => {

            console.error('Error:', error.response ? error.response.data : error.message);
        })
    }


    function getAllUsers() {
        axios.get(`${apiBaseUrl}/chat/allUsers`, {
            headers: {'Content-Type': 'application/json'},
            withCredentials: true
        }).then((response) => {
            // response.data.filter(u => {u._id === currChat._id});
            setAllUsers(response.data);
            // console.log('get Response ', response);
        }).catch((error) => {
            console.error('Error:', error.response ? error.response.data : error.message);
            toast.error(error.response ? error.response.data : error.message, {duration: 1000});
        })
    }

    return (
        <>
            <div className="flex h-screen">
                <div className="flex flex-col border-r border-r-gray-300 w-3/12">
                    <div className="flex flex-row justify-between items-center px-4 py-2 border-b border-b-gray-300">
                        <span className="text-lg font-semibold">Chat App</span>
                        <LogOut className={LucidClass} onClick={logOut}/>
                    </div>

                    <div className="px-5 py-2 flex flex-row justify-between">
                        <span className="text-lg font-normal">Groups and Chats</span>
                        <Plus className={LucidClass} onClick={handleOpenChatModal}/>
                        <Modal isOpen={isChatModalOpen} onClose={handleCloseChatModal} onSubmit={createChat}
                               title={"Create Chat"}>
                            <div>
                                <input
                                    type="text"
                                    value={newChatName}
                                    onChange={(e) => setNewChatName(e.target.value)}
                                    placeholder="Enter chat name "
                                    className="   w-full
    px-4 py-3
    bg-slate-100 dark:bg-slate-800
    text-slate-800 dark:text-slate-200
    placeholder:text-slate-500 dark:placeholder:text-slate-500
    border border-slate-300 dark:border-slate-600
    rounded-lg
    focus:outline-none
    focus:ring-2 focus:ring-blue-500
    focus:border-transparent
    transition-colors duration-200"
                                />
                                <br/>
                                <br/>
                                <span className={"font-normal ml-2"}>Select Members</span>
                                <br/>



                                {allUsers.filter(u=>u._id !==user?._id).map((user: any) => (
                                    <AddUser
                                        key={user._id}
                                        user={user}
                                        isSelected={chatUsers.some(u => u._id === user._id)}
                                        onClick={() => addChat(user)}
                                    />
                                ))}
                            </div>
                        </Modal>

                    </div>

                    <div className="px-5 py-2 flex flex-col justify-between overflow-y-auto">
                        {chats.map((chat: any, index: number) => (
                            <Chat
                                key={chat._id || index}
                                chat={chat}
                                onClick={() => setCurrChat(chat)}
                                activeChat={currChat._id === chat._id}
                            />
                        ))}
                    </div>
                </div>

                <div className="flex flex-col w-9/12">
                    <MessageArea message={Messages}/>
                </div>
            </div>
        </>

    );
}

export default Dashboard;
