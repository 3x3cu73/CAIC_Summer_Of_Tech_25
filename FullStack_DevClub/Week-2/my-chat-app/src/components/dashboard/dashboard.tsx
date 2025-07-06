import { useEffect, useState, useRef } from "react";
import { Send, Users, MessageCircle, Settings, LogOut, Search, Plus } from "lucide-react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(false); // null = loading, true = logged in, false = not logged in
    const [currentUser] = useState({ id: 1, name: "You", avatar: "🧑‍💻" });
    const [selectedGroup, setSelectedGroup] = useState(1);
    const [message, setMessage] = useState("");
    const [searchTerm, setSearchTerm] = useState("");
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    // Authentication check (uncomment and modify as needed)
    useEffect(() => {
        // Simulate API call - replace with your actual authentication logic
        const checkAuth = async () => {
            try {
                const apiBaseUrl = import.meta.env.VITE_API_BASE;
                const response = await axios.post(`${apiBaseUrl}/validate`, {}, {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true,
                });

                // For demo purposes, simulating successful login after 1 second
                setIsLoggedIn(response.data.status)
            } catch (error) {
                setIsLoggedIn(false);
            }
        };

        checkAuth();
    }, []);

    // Redirect if not logged in
    useEffect(() => {
        if (isLoggedIn === false) {
            // navigate('/login'); // Uncomment when using with router
            console.log('Redirecting to login...');
        }
    }, [isLoggedIn]);
    // Mock data for demonstration
    const [groups] = useState([
        { id: 1, name: "General", members: 12, lastMessage: "Hey everyone! 👋", unread: 3 },
        { id: 2, name: "Development Team", members: 8, lastMessage: "The new feature is ready for testing", unread: 0 },
        { id: 3, name: "Marketing", members: 5, lastMessage: "Campaign results look great!", unread: 1 },
        { id: 4, name: "Design Team", members: 6, lastMessage: "New mockups uploaded", unread: 2 }
    ]);

    const [messages, setMessages] = useState([
        { id: 1, groupId: 1, userId: 2, userName: "Alice", avatar: "👩‍💼", content: "Good morning everyone!", timestamp: "09:30 AM", type: "text" },
        { id: 2, groupId: 1, userId: 3, userName: "Bob", avatar: "👨‍💻", content: "Hey! Ready for the sprint planning?", timestamp: "09:32 AM", type: "text" },
        { id: 3, groupId: 1, userId: 1, userName: "You", avatar: "🧑‍💻", content: "Absolutely! Looking forward to it", timestamp: "09:35 AM", type: "text" },
        { id: 4, groupId: 1, userId: 4, userName: "Carol", avatar: "👩‍🎨", content: "I've prepared the design updates", timestamp: "09:38 AM", type: "text" },
        { id: 5, groupId: 1, userId: 2, userName: "Alice", avatar: "👩‍💼", content: "Perfect! Let's start in 5 minutes", timestamp: "09:40 AM", type: "text" },
        { id: 6, groupId: 2, userId: 3, userName: "Bob", avatar: "👨‍💻", content: "The API integration is complete", timestamp: "10:15 AM", type: "text" },
        { id: 7, groupId: 2, userId: 5, userName: "David", avatar: "👨‍🔬", content: "Great work! I'll start the testing phase", timestamp: "10:20 AM", type: "text" }
    ]);

    const [onlineUsers] = useState([
        { id: 1, name: "You", avatar: "🧑‍💻", status: "online" },
        { id: 2, name: "Alice", avatar: "👩‍💼", status: "online" },
        { id: 3, name: "Bob", avatar: "👨‍💻", status: "online" },
        { id: 4, name: "Carol", avatar: "👩‍🎨", status: "away" },
        { id: 5, name: "David", avatar: "👨‍🔬", status: "online" },
        { id: 6, name: "Eve", avatar: "👩‍🔬", status: "offline" }
    ]);

    const filteredMessages = messages.filter(msg => msg.groupId === selectedGroup);
    const currentGroup = groups.find(g => g.id === selectedGroup);

    useEffect(() => {
        scrollToBottom();
    }, [filteredMessages]);

    const scrollToBottom = () => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({
                behavior: "smooth",
                block: "end",
                inline: "nearest"
            })
        }
    };

    const handleSendMessage = (e:any) => {
        e.preventDefault();
        if (!message.trim()) return;

        const newMessage = {
            id: messages.length + 1,
            groupId: selectedGroup,
            userId: currentUser.id,
            userName: currentUser.name,
            avatar: currentUser.avatar,
            content: message,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            type: "text"
        };

        setMessages(prev => [...prev, newMessage]);
        setMessage("");
    };

    const getStatusColor = (status:any) => {
        switch (status) {
            case 'online': return 'bg-green-500';
            case 'away': return 'bg-yellow-500';
            default: return 'bg-gray-400';
        }
    };

    // Show loading state while checking authentication
    if (isLoggedIn === null) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-gray-600">Checking authentication...</p>
                </div>
            </div>
        );
    }

    // Show login message if not authenticated
    if (!isLoggedIn) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-100">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Access Denied</h2>
                    <p className="text-gray-600 mb-4">Please log in to access the chat dashboard.</p>
                    <button className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors" onClick={() => navigate('/login')}
                    >
                        Go to Login
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
                {/* Header */}
                <div className="p-4 border-b border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                        <h1 className="text-xl font-bold text-gray-800">Chat Dashboard</h1>
                        <div className="flex space-x-2">
                            <button className="p-2 hover:bg-gray-100 rounded-lg">
                                <Settings className="w-5 h-5 text-gray-600" />
                            </button>
                            <button className="p-2 hover:bg-gray-100 rounded-lg">
                                <LogOut className="w-5 h-5 text-gray-600" />
                            </button>
                        </div>
                    </div>

                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search groups..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                </div>

                {/* Groups List */}
                <div className="flex-1 overflow-y-auto">
                    <div className="p-4">
                        <div className="flex items-center justify-between mb-3">
                            <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider">Groups</h2>
                            <button className="p-1 hover:bg-gray-100 rounded">
                                <Plus className="w-4 h-4 text-gray-600" />
                            </button>
                        </div>

                        <div className="space-y-2">
                            {groups.map(group => (
                                <button
                                    key={group.id}
                                    onClick={() => setSelectedGroup(group.id)}
                                    className={`w-full p-3 rounded-lg text-left transition-colors ${
                                        selectedGroup === group.id
                                            ? 'bg-blue-50 border-2 border-blue-200'
                                            : 'hover:bg-gray-50 border-2 border-transparent'
                                    }`}
                                >
                                    <div className="flex items-center justify-between mb-1">
                                        <div className="flex items-center space-x-2">
                                            <MessageCircle className="w-4 h-4 text-gray-500" />
                                            <span className="font-medium text-gray-800">{group.name}</span>
                                        </div>
                                        {group.unread > 0 && (
                                            <span className="bg-blue-500 text-white text-xs px-2 py-1 rounded-full">
                                                {group.unread}
                                            </span>
                                        )}
                                    </div>
                                    <div className="flex items-center justify-between text-sm text-gray-500">
                                        <span className="truncate">{group.lastMessage}</span>
                                        <span className="flex items-center space-x-1">
                                            <Users className="w-3 h-3" />
                                            <span>{group.members}</span>
                                        </span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Online Users */}
                <div className="p-4 border-t border-gray-200">
                    <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wider mb-3">Online Users</h3>
                    <div className="space-y-2 max-h-32 overflow-y-auto">
                        {onlineUsers.filter(user => user.status === 'online').map(user => (
                            <div key={user.id} className="flex items-center space-x-2">
                                <div className="relative">
                                    <span className="text-sm">{user.avatar}</span>
                                    <div className={`absolute -bottom-1 -right-1 w-3 h-3 rounded-full border-2 border-white ${getStatusColor(user.status)}`}></div>
                                </div>
                                <span className="text-sm text-gray-700">{user.name}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col">
                {/* Chat Header */}
                <div className="bg-white border-b border-gray-200 p-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <MessageCircle className="w-6 h-6 text-blue-500" />
                            <div>
                                <h2 className="font-semibold text-gray-800">{currentGroup?.name}</h2>
                                <p className="text-sm text-gray-500">{currentGroup?.members} members</p>
                            </div>
                        </div>
                        <div className="flex items-center space-x-2">
                            <button className="p-2 hover:bg-gray-100 rounded-lg">
                                <Users className="w-5 h-5 text-gray-600" />
                            </button>
                            <button className="p-2 hover:bg-gray-100 rounded-lg">
                                <Search className="w-5 h-5 text-gray-600" />
                            </button>
                        </div>
                    </div>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {filteredMessages.map(msg => (
                        <div key={msg.id} className={`flex items-start space-x-3 ${msg.userId === currentUser.id ? 'flex-row-reverse space-x-reverse' : ''}`}>
                            <div className="flex-shrink-0">
                                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm">
                                    {msg.avatar}
                                </div>
                            </div>
                            <div className={`flex-1 ${msg.userId === currentUser.id ? 'text-right' : ''}`}>
                                <div className="flex items-center space-x-2 mb-1">
                                    <span className="text-sm font-medium text-gray-800">{msg.userName}</span>
                                    <span className="text-xs text-gray-500">{msg.timestamp}</span>
                                </div>
                                <div className={`inline-block px-4 py-2 rounded-lg max-w-md ${
                                    msg.userId === currentUser.id
                                        ? 'bg-blue-500 text-white'
                                        : 'bg-gray-200 text-gray-800'
                                }`}>
                                    {msg.content}
                                </div>
                            </div>
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>

                {/* Message Input */}
                <div className="bg-white border-t border-gray-200 p-4">
                    <div className="flex items-center space-x-3">
                        <div className="flex-1 relative">
                            <input
                                type="text"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage(e)}
                                placeholder={`Message ${currentGroup?.name}...`}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                        <button
                            onClick={handleSendMessage}
                            disabled={!message.trim()}
                            className="p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
