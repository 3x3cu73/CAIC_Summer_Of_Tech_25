import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { Send, Loader2 } from 'lucide-react';
import type { Message } from "../types/chat"; // Make sure path is correct

const apiBaseUrl = import.meta.env.VITE_API_BASE;

type MessageInputProps = {
    chatId: string;
    setMessages: (updateFn: (prev: Message[]) => Message[]) => void;
};

function MessageInput({ chatId, setMessages }: MessageInputProps) {
    const [content, setContent] = useState("");
    const [isSending, setIsSending] = useState(false);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    // --- Effect for auto-growing textarea ---
    // This adjusts the textarea height based on its content.
    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = 'auto'; // Reset height to recalculate
            textarea.style.height = `${textarea.scrollHeight}px`; // Set to new content height
        }
    }, [content]);

    // --- Function to send the message via HTTP ---
    const sendMessage = () => {
        if (!content.trim() || isSending) return; // Prevent sending empty or during submission

        setIsSending(true);
        axios
            .post(`${apiBaseUrl}/chat/sendMessage`, { content: content.trim(), chatId }, { withCredentials: true })
            .then((response) => {
                setContent(""); // Clear input on success
                // Update the parent component's message list with the new message from the server
                setMessages((prev) => [...prev, response.data]);
            })
            .catch((err) => {
                toast.error(err?.response?.data?.message || "Failed to send message");
            })
            .finally(() => {
                setIsSending(false);
            });
    };

    // --- Handler for keyboard events ---
    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        // Send message on 'Enter' but allow new lines with 'Shift + Enter'
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // Prevents adding a new line in the textarea
            sendMessage();
        }
    };

    return (
        <div className="p-3 md:p-4 bg-white border-t border-slate-200 shadow-inner">
            <div className="flex items-end gap-3">
                <textarea
                    ref={textareaRef}
                    rows={1}
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type a message..."
                    className="flex-grow p-3 bg-slate-100 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all max-h-40 overflow-y-auto"
                    disabled={isSending}
                />
                <button
                    onClick={sendMessage}
                    disabled={!content.trim() || isSending}
                    className="flex-shrink-0 flex items-center justify-center w-12 h-12 bg-indigo-600 text-white rounded-full transition-all duration-200 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-slate-400 focus:outline-none focus:ring-4 focus:ring-indigo-300"
                    aria-label="Send Message"
                >
                    {isSending ? (
                        <Loader2 size={22} className="animate-spin" />
                    ) : (
                        <Send size={22} className="transform -rotate-12" />
                    )}
                </button>
            </div>
        </div>
    );
}

export default MessageInput;
