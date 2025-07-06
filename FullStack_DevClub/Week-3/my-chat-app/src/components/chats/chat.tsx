import React from "react";
import {useUser} from "../../context/userContext.tsx";

type ChatProps = {
    chat: any;
    activeChat: any,
} & React.HTMLAttributes<HTMLDivElement>;

function Chat({ chat,activeChat, ...props }: ChatProps) {
    const {user} = useUser()

    if (!chat.isGroupChat) {
        let person = chat.participants.filter((person: { username: string; }) => person.username !== user?.username)[0];
        chat.name =person.username;
    }


    chat.unreadCount = 2;

    return (
        <div
            {...props}
            className={`border-2 ${
            activeChat ? "border-blue-300" : "border-transparent"
        } cursor-pointer px-4 py-2 rounded-sm m-1 flex flex-col ${props.className || ""}`}


        >
            <div className="flex flex-row justify-between items-center">
                <div className="font-normal text-sm">{chat.name}</div>
                {chat.unreadCount > 0 && (
                    <div className="w-5 h-5 rounded-full bg-blue-400 text-white text-xs flex items-center justify-center">
                        {chat.unreadCount}
                    </div>
                )}
            </div>
            <div>
                <div className="text-xs text-gray-700">
                    {chat.participants.find((p: any) => p._id === chat.latestMessage.sender)?.username} :

                <span className="text-xs text-gray-500">
                    {chat.latestMessage.content}
                </span>
                </div>
            </div>
        </div>
    );
}

export default Chat;
