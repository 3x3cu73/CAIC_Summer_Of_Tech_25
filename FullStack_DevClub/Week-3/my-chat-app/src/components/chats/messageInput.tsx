import LoadingButton from "../ui/button.tsx";
import { Send } from 'lucide-react';
import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import type { Message } from "../types/chat";

const apiBaseUrl = import.meta.env.VITE_API_BASE;

function MessageInput({
                          chatId,
                          setMessages,
                      }: {
    chatId: string;
    setMessages?: (updateFn: (prev: Message[]) => Message[]) => void;
}) {
    const [content, setContent] = useState("");
    const [isSending, setSending] = useState(false);

    const sendMessage = () => {
        if (!content.trim()) return;
        setSending(true);
        axios
            .post(`${apiBaseUrl}/chat/sendMessage`, { content, chatId }, { withCredentials: true })
            .then((response) => {
                setSending(false);
                setContent("");
                setMessages?.((prev) => [...prev, response.data]);
            })
            .catch((err) => {
                setSending(false);
                toast.error(err?.response?.data?.message || "Message failed");
            });
    };

    return (
        <div className="p-4 bg-white border-t border-gray-200">
            <div className="flex items-center space-x-3">
                <input
                    type="text"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Type a message..."
                    className="flex-grow px-4 py-2 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={isSending}
                />
                <LoadingButton loading={isSending} loadText={""} className={"rounded-xl"} onClick={sendMessage}>
                    <Send />
                </LoadingButton>
            </div>
        </div>
    );
}

export default MessageInput;
