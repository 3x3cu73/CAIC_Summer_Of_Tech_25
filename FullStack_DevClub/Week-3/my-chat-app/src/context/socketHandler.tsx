import React, { createContext, useContext, useEffect, useRef } from "react";
import io from "socket.io-client";
import type { Socket } from "socket.io-client";
import {useUser} from "./userContext.tsx";

const SocketContext = createContext<typeof Socket | null>(null);
export const useSocket = () => useContext(SocketContext);

export const SocketProvider: React.FC<{ children: React.ReactNode;  }> = ({ children }) => {
    const socketRef = useRef<typeof Socket | null>(null);
    const {user} = useUser();
    const userId = user?._id;

    useEffect(() => {
        console.log("User Id is : " , userId);
        if (!userId) return;

        const socket = io(import.meta.env.VITE_API_BASE.replace(/\/chatApp\/?$/, ""), {
            path: "/chatApp/socket.io",
            // withCredentials: true,
        });

        socketRef.current = socket;


        socket.on("connect", () => {
            console.log(" Socket connected successfully:", socket.id);
            socket.emit("setup", userId);
        });

        socket.on("connected", () => {
            console.log("Setup completed for user:", userId);
        });

        socket.on("disconnect", (reason: any) => {
            console.log("Socket disconnected:", reason);
        });

        socket.on("connect_error", (error: any) => {
            console.error("Socket connection error:", error);
            console.log("Connection URL:", socket.io.uri);
        });

        console.log("Attempting to connect to socket...");

        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
                socketRef.current = null;
            }
        };
    }, [userId]);

    return (
        <SocketContext.Provider value={socketRef.current}>
            {children}
        </SocketContext.Provider>
    );
};

