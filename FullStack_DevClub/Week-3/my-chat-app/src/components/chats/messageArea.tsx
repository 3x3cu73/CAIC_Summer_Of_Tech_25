import React from "react";
import { useUser } from "../../context/userContext.tsx";
import type { Message } from "../types/chat";
import MessageInput from "./messageInput.tsx";




type MessageAreaProps = {
    messages: Message[];
    chatId: string;
    setMessages: (updater: (prev: Message[]) => Message[]) => void;
} & React.HTMLAttributes<HTMLDivElement>;

function MessageArea({ messages = [],setMessages,chatId, ...props }: MessageAreaProps) {

    const { user } = useUser();


    const formatTime = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };


    if (!user) {
        return <div className="flex-grow flex items-center justify-center">Loading messages...</div>;
    }

    return (
        <>
        <div
            {...props}
            className="flex flex-col flex-grow p-4 overflow-y-auto bg-gray-50 space-y-4"
        >
            {messages.map((message) => {

                const isCurrentUserSender = message.sender._id === user._id;

                return (

                    <div
                        key={message._id}
                        className={`flex flex-col ${
                            isCurrentUserSender ? 'items-end' : 'items-start'
                        }`}
                    >

                        {!isCurrentUserSender && (
                            <div className="text-xs text-gray-500 ml-2 mb-1">
                                {message.sender.username}
                            </div>
                        )}


                        <div
                            className={`rounded-xl px-4 py-2 max-w-lg ${
                                isCurrentUserSender
                                    ? 'bg-blue-500 text-white rounded-br-none' 
                                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                            }`}
                        >
                            <p className="text-base break-words">{message.content}</p>
                            <p
                                className={`text-xs mt-1 text-right opacity-70 ${
                                    isCurrentUserSender ? 'text-blue-100' : 'text-gray-500'
                                }`}
                            >
                                {formatTime(message.createdAt)}
                            </p>
                        </div>
                    </div>
                );
            })}

        </div>
<MessageInput chatId={chatId} setMessages={setMessages} />
        </>
    );
}

export default MessageArea;
