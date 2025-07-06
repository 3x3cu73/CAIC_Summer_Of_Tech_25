import React from "react";
import { useUser } from "../../context/userContext.tsx"; // Your user context hook
import type { Message } from "../types/chat"; // Adjust path to your types file



// Props now expect an array of the new Message type
type MessageAreaProps = {
    messages: Message[];
} & React.HTMLAttributes<HTMLDivElement>;

function MessageArea({ messages = [], ...props }: MessageAreaProps) {
    // Get the currently logged-in user from your context
    const { user } = useUser();

    // A helper to format the date.
    // You can replace this with a library like `date-fns` for more complex needs.
    const formatTime = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    // If the user data is not yet loaded, you can show a loading state or return null
    if (!user) {
        return <div className="flex-grow flex items-center justify-center">Loading messages...</div>;
    }

    return (
        // Main scrollable container for all messages
        <div
            {...props}
            className="flex flex-col flex-grow p-4 overflow-y-auto bg-gray-50 space-y-4"
        >
            {messages.map((message) => {
                // Check if the message was sent by the currently logged-in user
                const isCurrentUserSender = message.sender._id === user._id;

                return (
                    // Container for each message to handle alignment
                    <div
                        key={message._id}
                        className={`flex flex-col ${
                            isCurrentUserSender ? 'items-end' : 'items-start'
                        }`}
                    >
                        {/* Display sender's username above the bubble if it's not the current user */}
                        {!isCurrentUserSender && (
                            <div className="text-xs text-gray-500 ml-2 mb-1">
                                {message.sender.username}
                            </div>
                        )}

                        {/* The message bubble */}
                        <div
                            className={`rounded-xl px-4 py-2 max-w-lg ${
                                isCurrentUserSender
                                    ? 'bg-blue-500 text-white rounded-br-none' // Style for sender
                                    : 'bg-gray-200 text-gray-800 rounded-bl-none' // Style for receiver
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
    );
}

export default MessageArea;
