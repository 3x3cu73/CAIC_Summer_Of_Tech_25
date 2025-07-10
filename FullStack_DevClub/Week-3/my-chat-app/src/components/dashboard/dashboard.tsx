import { useEffect, useState } from "react";
import { LogOut, Plus, Search, Users, MessageSquarePlus, Video, VideoOff, X } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import Chat from "../chats/chat.tsx";
import MessageArea from "../chats/messageArea.tsx";
import Modal from "../modal/modal.tsx";
import AddUser from "../chats/addUser.tsx";
import { useUser } from "../../context/userContext.tsx";
import VideoCall from "../chats/VideoCall.tsx";

const apiBaseUrl = import.meta.env.VITE_API_BASE;

const UserAvatar = ({ name, size = 'w-11 h-11' }: { name?: string, size?: string }) => {
    if (!name) return <div className={`${size} bg-slate-300 rounded-full`}></div>;
    const initial = name.charAt(0).toUpperCase();
    const colorIndex = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 5;
    const colors = [
        'from-indigo-500 to-blue-500',
        'from-green-500 to-emerald-500',
        'from-purple-500 to-violet-500',
        'from-red-500 to-rose-500',
        'from-amber-500 to-orange-500',
    ];
    return (
        <div className={`rounded-full flex items-center justify-center text-white font-bold bg-gradient-to-br ${size} ${colors[colorIndex]}`}>
            <span style={{ fontSize: `calc(${size.replace('w-', '')}rem / 2.5)` }}>{initial}</span>
        </div>
    );
};

const ChatListSkeleton = () => (
    <div className="px-3 space-y-3 mt-4">
        {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center gap-3 animate-pulse">
                <div className="w-11 h-11 bg-slate-200 rounded-full"></div>
                <div className="flex-1">
                    <div className="h-4 bg-slate-200 rounded w-3/4"></div>
                    <div className="h-3 bg-slate-200 rounded w-1/2 mt-2"></div>
                </div>
            </div>
        ))}
    </div>
);

const VideoCallModal = ({ chat, onClose }) => (
    <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm z-40 flex items-center justify-center p-2 sm:p-4 transition-opacity duration-300"
        style={{ animation: 'fadeIn 0.3s ease-out' }}
    >
        <div className="relative w-full h-full max-w-7xl bg-slate-900 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
            <header className="flex items-center justify-between p-3 border-b border-slate-700 flex-shrink-0">
                <div className="flex items-center gap-3">
                    <Video className="text-indigo-400" size={20} />
                    <h3 className="font-bold text-white truncate">
                        <span className="hidden sm:inline">Video Call: </span>{chat.name}
                    </h3>
                </div>
                <button
                    onClick={onClose}
                    className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg transition-colors bg-red-500 text-white hover:bg-red-600"
                >
                    <X size={18} />
                    <span className="hidden sm:inline">Leave Call</span>
                </button>
            </header>
            <div className="flex-1 min-h-0">
                {chat && <VideoCall chat={chat} />}
            </div>
        </div>
    </div>
);


function Dashboard() {
    const { user, loading: userLoading } = useUser();
    const navigate = useNavigate();

    const [chats, setChats] = useState<any[]>([]);
    const [currChat, setCurrChat] = useState<any>(null);
    const [messages, setMessages] = useState<any[]>([]);
    const [isChatLoading, setIsChatLoading] = useState<boolean>(true);
    const [searchQuery, setSearchQuery] = useState<string>('');
    const [isVideoCallActive, setVideoCallActive] = useState(false);
    const [isChatModalOpen, setIsChatModalOpen] = useState(false);
    const [allUsers, setAllUsers] = useState<any[]>([]);
    const [chatUsers, setChatUsers] = useState<any[]>([]);
    const [newChatName, setNewChatName] = useState<string>('');

    useEffect(() => {
        if (!userLoading && !user?.username) {
            const timer = setTimeout(() => {
                if (!user?.username) {
                    window.location.reload();
                }
            }, 2000);
            return () => clearTimeout(timer);
        }
    }, [userLoading, user]);

    useEffect(() => {
        axios.post(`${apiBaseUrl}/auth/validate`, {}, { withCredentials: true })
            .catch(() => {
                toast.error('Session expired. Please log in again.');
                navigate('/login');
            });
    }, [navigate]);

    const fetchChats = () => {
        if (!user?._id) return;
        setIsChatLoading(true);
        axios.post(`${apiBaseUrl}/chat/getChats`, {}, { withCredentials: true })
            .then((response) => {
                setChats(response.data);
                if (response.data.length > 0 && !currChat) {
                    setCurrChat(response.data[0]);
                }
            })
            .catch(() => toast.error("Could not fetch your chats."))
            .finally(() => setIsChatLoading(false));
    };

    useEffect(() => {
        fetchChats();
    }, [user]);

    useEffect(() => {
        if (currChat?._id) {
            axios.post(`${apiBaseUrl}/chat/getMessages`, { chat: currChat._id }, { withCredentials: true })
                .then((response) => setMessages(response.data))
                .catch((error) => console.error('Error fetching messages:', error));
        } else {
            setMessages([]);
        }
    }, [currChat?._id]);

    useEffect(() => {
        if (!userLoading && user) setChatUsers([user]);
    }, [userLoading, user]);

    const handleOpenChatModal = () => {
        if (allUsers.length === 0) getAllUsers();
        setIsChatModalOpen(true);
    };

    const handleCloseChatModal = () => {
        setIsChatModalOpen(false);
        setNewChatName('');
        if (user) setChatUsers([user]);
    };

    const getAllUsers = () => {
        axios.get(`${apiBaseUrl}/chat/allUsers`, { withCredentials: true })
            .then((response) => setAllUsers(response.data))
            .catch(() => toast.error("Could not fetch users."));
    };

    const addChatUser = (selectedUser: any) => {
        setChatUsers(prev =>
            prev.some(u => u._id === selectedUser._id)
                ? prev.filter(u => u._id !== selectedUser._id)
                : [...prev, selectedUser]
        );
    };

    const createChat = () => {
        if (!newChatName.trim() || chatUsers.length < 2) {
            toast.error("Please provide a chat name and select at least one other member.");
            return;
        }
        axios.post(`${apiBaseUrl}/chat/newChat`, { name: newChatName, participants: chatUsers.map(user => user._id) }, { withCredentials: true })
            .then(res => {
                toast.success(res.data.message);
                const newChat = res.data.chat;
                setCurrChat(newChat);
                handleCloseChatModal();
                setChats(prev => [newChat, ...prev]);
            })
            .catch(err => toast.error(err.response.data.message));
    };

    const logOut = () => {
        axios.post(`${apiBaseUrl}/auth/logout`, {}, { withCredentials: true })
            .then(() => {
                toast.success('You have been logged out.');
                navigate('/login');
            })
            .catch((error) => console.error('Logout Error:', error));
    };

    const handleChatSelect = (chat: any) => {
        if (currChat?._id !== chat._id) {
            setVideoCallActive(false);
        }
        setCurrChat(chat);
    };

    const filteredChats = chats.filter(chat =>
        chat?.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="flex h-screen font-sans bg-slate-100">
            <aside className="flex flex-col w-full md:w-80 lg:w-96 bg-white text-slate-800 border-r border-slate-200">
                <header className="flex items-center justify-between p-4 border-b border-slate-200 shadow-sm">
                    <div className="flex items-center gap-3">
                        <MessageSquarePlus className="text-indigo-500" size={28} />
                        <h1 className="text-xl font-bold tracking-wider text-slate-800">ChatApp</h1>
                    </div>
                    <button onClick={handleOpenChatModal} className="p-2 rounded-full text-slate-500 hover:bg-slate-100 hover:text-indigo-500 transition-colors" title="Create New Chat">
                        <Plus size={22} />
                    </button>
                </header>
                <div className="p-3 border-b border-slate-200">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                        <input type="text" placeholder="Search chats..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="w-full bg-slate-100 border border-transparent rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white focus:border-indigo-500 text-slate-700 placeholder:text-slate-500 transition" />
                    </div>
                </div>
                <div className="flex-grow overflow-y-auto">
                    {isChatLoading ? <ChatListSkeleton /> : (
                        <div className="px-3 space-y-1 py-2">
                            {filteredChats.map((chat: any) => (
                                <Chat key={chat._id} chat={chat} onClick={() => handleChatSelect(chat)} activeChat={currChat?._id === chat._id} AvatarComponent={<UserAvatar name={chat.name} />} />
                            ))}
                        </div>
                    )}
                </div>
                <footer className="flex items-center gap-3 p-4 mt-auto border-t border-slate-200">
                    {!userLoading && user && <UserAvatar name={user.username} />}
                    <div className="flex-grow overflow-hidden">
                        <p className="font-semibold text-slate-700 truncate">{user?.username || 'Loading...'}</p>
                        <p className="text-xs text-green-500">Online</p>
                    </div>
                    <button onClick={logOut} title="Log Out" className="p-2 rounded-full text-slate-500 hover:bg-slate-100 hover:text-rose-500 transition-colors">
                        <LogOut size={20} />
                    </button>
                </footer>
            </aside>
            <main className="flex-col flex-grow hidden md:flex relative">
                {currChat ? (
                    <>
                        <header className="flex items-center justify-between gap-4 p-4 bg-white border-b border-slate-200 shadow-sm">
                            <div className="flex items-center gap-4">
                                <UserAvatar name={currChat.name} />
                                <div>
                                    <h2 className="text-lg font-bold text-slate-800">{currChat.name}</h2>
                                    <div className="flex items-center gap-1 text-sm text-slate-500">
                                        <Users size={14} />
                                        <span>{currChat.participants.length} Members</span>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setVideoCallActive(prev => !prev)}
                                className={`flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg transition-all ${
                                    isVideoCallActive
                                        ? 'bg-red-100 text-red-700 hover:bg-red-200'
                                        : 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200'
                                }`}
                            >
                                {isVideoCallActive ? <VideoOff size={18} /> : <Video size={18} />}
                                <span>{isVideoCallActive ? 'Leave Call' : 'Join Call'}</span>
                            </button>
                        </header>
                        <div className="flex flex-col flex-grow overflow-hidden">
                            <MessageArea messages={messages} chat={currChat} setMessages={setMessages} />
                        </div>

                        {isVideoCallActive && (
                            <VideoCallModal chat={currChat} onClose={() => setVideoCallActive(false)} />
                        )}
                    </>
                ) : (
                    <div className="flex flex-col items-center justify-center h-full text-center bg-slate-50">
                        <UserAvatar name="ChatApp" size="w-24 h-24" />
                        <h2 className="mt-6 text-2xl font-semibold text-slate-700">Welcome to ChatApp</h2>
                        <p className="mt-2 text-slate-500">Select a chat to start messaging.</p>
                        <button onClick={handleOpenChatModal} className="mt-6 flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors shadow-sm hover:shadow-md">
                            <Plus size={20} /> Create a New Chat
                        </button>
                    </div>
                )}
            </main>
            <Modal isOpen={isChatModalOpen} onClose={handleCloseChatModal} onSubmit={createChat} title="Create a New Chat">
                <div className="space-y-4">
                    <input type="text" value={newChatName} onChange={(e) => setNewChatName(e.target.value)} placeholder="Enter chat name (e.g., Project Team)" className="w-full px-4 py-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 outline-none bg-white text-slate-700" />
                    <div>
                        <p className="font-semibold text-slate-600">Select Members:</p>
                        <div className="mt-2 max-h-60 overflow-y-auto p-1 rounded-md border border-slate-200 bg-slate-50 space-y-1">
                            {allUsers.filter(u => u._id !== user?._id).map((u: any) => (
                                <AddUser key={u._id} user={u} isSelected={chatUsers.some(cu => cu._id === u._id)} onClick={() => addChatUser(u)} AvatarComponent={<UserAvatar name={u.username} size="w-10 h-10" />} />
                            ))}
                        </div>
                    </div>
                </div>
            </Modal>
        </div>
    );
}

export default Dashboard;
