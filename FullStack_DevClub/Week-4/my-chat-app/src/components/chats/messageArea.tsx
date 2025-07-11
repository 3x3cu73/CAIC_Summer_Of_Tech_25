import React, { useEffect, useRef } from "react";
import { useUser } from "../../context/userContext.tsx";
import type { Message } from "../types/chat";
import MessageInput from "./messageInput.tsx";
import { Loader2 } from "lucide-react";
import {useSocket} from "../../context/socketHandler.tsx";


type MessageAreaProps = {
    messages: Message[];
    chat:any;
    setMessages: (updater: (prev: any) => (Message | {
        chat: any;
        _id?: string;
        content?: string;
        sender?: { _id: string; username: string };
        createdAt?: string;
        updatedAt?: string
    })[]) => void;
} & React.HTMLAttributes<HTMLDivElement>;

function MessageArea({ messages = [], setMessages,chat, ...props }: MessageAreaProps) {
    const { user, loading: userLoading } = useUser();
    const messagesEndRef = useRef<null | HTMLDivElement>(null);

    const chatId = chat._id;
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };


    useEffect(() => {
        scrollToBottom();
    }, [messages]);


    const socket = useSocket();
    useEffect(() => {
        if (!socket ) {
            console.warn("Socket missing");
            return;
        }
        if (!chatId){
            console.warn("No chatId found.");
            return;
        }

        socket.emit("joinChat", chatId, (response: any) => {
            console.log("Acknowledgment received:", response);

            if (response?.success) {
                console.log("Joined Chat:", chatId);
            } else {
                console.error("Failed to join chat:", response?.message || "Unknown error");
            }
        });

        return () => {
            socket.emit("leaveChat", chatId);
        };
    }, [socket, chatId]);

    useEffect(() => {
        if (!socket) return;

        const handler = (msg: { chat: any; _id?: string; content?: string; sender?: { _id: string; username: string; }; createdAt?: string; updatedAt?: string; }) => {
            if (msg.chat._id === chatId) {
                setMessages(prev => [...prev, msg]);
            }
        };

        socket.on("receiveMessage", handler);

        return () => {
            socket.off("receiveMessage", handler);
        };
    }, [socket, chatId]);


    const formatTime = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };


    if (userLoading || !user) {
        return (
            <div className="flex-grow flex items-center justify-center text-slate-500 bg-slate-50">
                <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
            </div>
        );
    }

    return (
        <>
            <div
                {...props}
                className="flex-grow p-4 md:p-6 overflow-y-auto bg-slate-100">
                <div className="flex flex-col gap-y-2">
                    {messages.map((message, index) => {
                        const isCurrentUserSender = message.sender._id === user._id;


                        const prevMessage = messages[index - 1];
                        const nextMessage = messages[index + 1];

                        const isFirstInGroup = !prevMessage || prevMessage.sender._id !== message.sender._id;
                        const isLastInGroup = !nextMessage || nextMessage.sender._id !== message.sender._id;


                        if (isCurrentUserSender) {
                        } else {
                        }


                        const tailClass = isLastInGroup ? (isCurrentUserSender ? 'rounded-br-none' : 'rounded-bl-none') : '';


                        return (
                            <div
                                key={message._id}
                                className={`flex flex-col ${isCurrentUserSender ? 'items-end' : 'items-start'}`}
                            >
                                {/* Show sender's name only for the first message in a group */}
                                {isFirstInGroup && !isCurrentUserSender && (
                                    <div className="text-xs text-slate-500 ml-3 mb-1 font-medium">
                                        {message.sender.username}
                                    </div>
                                )}

                                <div
                                    className={`
                                        rounded-xl px-4 py-2.5 max-w-lg md:max-w-2xl
                                        ${tailClass}
                                        ${isCurrentUserSender
                                        ? 'bg-indigo-600 text-white'
                                        : 'bg-white text-slate-800 border border-slate-200'
                                    }
                                        ${isFirstInGroup && isCurrentUserSender ? 'mt-3' : ''}
                                    `}
                                >

                                    <p className="text-base break-words whitespace-pre-wrap">{message.content}</p>


                                    {isLastInGroup && (
                                        <p className={`
                                            text-xs mt-1 text-right opacity-80
                                            ${isCurrentUserSender ? 'text-indigo-200' : 'text-slate-400'}
                                        `}>
                                            {formatTime(message.createdAt)}
                                        </p>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>

                <div ref={messagesEndRef} />
            </div>

            <MessageInput chatId={chatId} setMessages={setMessages} />
        </>
    );
}

export default MessageArea;
