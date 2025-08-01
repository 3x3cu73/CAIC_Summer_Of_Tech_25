import React from "react";
import { useUser } from "../../context/userContext.tsx";

type ChatProps = {
    chat: any;
    activeChat: boolean;
    AvatarComponent: React.ReactNode;
} & React.HTMLAttributes<HTMLDivElement>;

function Chat({ chat, activeChat, AvatarComponent, ...props }: ChatProps) {
    const { user } = useUser();
    if (chat && !chat.isGroupChat) {
        const person = chat.participants?.find((p: any) => p.username !== user?.username);
        if (person) {
            chat.name = person.username;
        }
    }



    if (!chat) {
        return null;
    }

    return (
        <div
            {...props}
            className={`
                flex items-center gap-3 p-2.5 rounded-lg cursor-pointer transition-colors duration-200
                // --- THEME CHANGE ---
                // Active state is now a subtle indigo, hover is a light slate gray.
                ${activeChat ? "bg-indigo-50" : "hover:bg-slate-100"}
            `}
        >

            <div className="flex-shrink-0">
                {AvatarComponent}
            </div>


            <div className="flex-grow min-w-0">

                <div className="flex justify-between items-center">
                    <h3 className={`
                        font-semibold truncate pr-2
                        // --- THEME CHANGE ---
                        // Text color is now dark slate, but becomes a stronger indigo when active.
                        ${activeChat ? "text-indigo-600" : "text-slate-800"}
                    `}>
                        {chat.name}
                    </h3>

                    {chat.unreadCount > 0 && (
                        <div className="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-500 text-white text-xs flex items-center justify-center font-bold">
                            {chat.unreadCount}
                        </div>
                    )}
                </div>


                <div className="mt-0.5">
                    {chat.latestMessage && (

                        <div className="text-sm text-slate-500 truncate">
                            <span className="font-semibold text-slate-600">
                                {chat.participants.find((p: any) => p._id === (typeof chat.latestMessage.sender === 'object' ? chat.latestMessage.sender._id : chat.latestMessage.sender))?.username}:
                            </span>
                            <span className="ml-1">{chat.latestMessage.content}</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Chat;
