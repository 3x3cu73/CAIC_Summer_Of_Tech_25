import { useState, useEffect } from 'react';
import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import { useSocket } from '../../context/socketHandler.js';
import { useUser } from '../../context/userContext.js';
import { Loader2, AlertTriangle } from 'lucide-react';


interface Chat {
    _id: string;
    name: string;
}

interface VideoCallProps {
    chat: Chat;
}

interface SocketResponse {
    success: boolean;
    token?: string;
    message?: string;
}

// --- Overlay for Loading and Error States ---
const CallOverlay = ({ children }: { children: React.ReactNode }) => (
    <div className="absolute inset-0 bg-slate-800 bg-opacity-80 flex flex-col items-center justify-center text-white z-10">
        {children}
    </div>
);

function VideoCall({ chat }: VideoCallProps) {
    const [token, setToken] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const socket = useSocket();
    const { user } = useUser();

    useEffect(() => {
        if (!socket || !user?._id || !chat?._id) {
            setError("Missing required data for video call.");
            setIsLoading(false);
            return;
        }

        setIsLoading(true);
        setError(null);
        // Request token for the selected chat
        socket.emit('join-video-room', {
            roomName: chat.name,
            roomId: chat._id,
            creator: user.username
        }, (response: SocketResponse) => {
            if (response.success && response.token) {
                setToken(response.token);
            } else {
                const errorMessage = response.message || "Failed to get video token.";
                console.error("Token Error:", errorMessage);
                setError(errorMessage);
            }
            setIsLoading(false);
        });

        // Cleanup function when chat changes or component unmounts
        return () => {
            setToken(null);
            setError(null);
            setIsLoading(true);
        };
    }, [socket, user?._id, user?.username, chat?._id, chat?.name]);

    // Use a relative container to position overlays
    return (
        <div className="relative h-full w-full bg-slate-900">
            {isLoading && (
                <CallOverlay>
                    <Loader2 className="w-8 h-8 animate-spin mb-4" />
                    <span>Joining video call...</span>
                </CallOverlay>
            )}

            {error && !isLoading && (
                <CallOverlay>
                    <AlertTriangle className="w-10 h-10 text-red-400 mb-4" />
                    <p className="text-red-300 mb-4 text-center px-4">Error: {error}</p>
                    <button
                        onClick={() => window.location.reload()} // Or a more specific retry function
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md transition-colors"
                    >
                        Retry Connection
                    </button>
                </CallOverlay>
            )}

            {token && (
                <LiveKitRoom
                    token={token}
                    serverUrl={import.meta.env.VITE_LIVEKIT_URL}
                    options={{ publishDefaults: { videoCodec: 'vp9' } }}
                    connectOptions={{
                        rtcConfig: {
                            iceServers: [{
                                urls: import.meta.env.VITE_TURN_URL,
                                username: import.meta.env.VITE_TURN_USERNAME,
                                credential: import.meta.env.VITE_TURN_PASSWORD,
                            }]
                        }
                    }}
                    video={true}
                    audio={true}
                    data-lk-theme="default"
                    style={{ height: '100%', width: '100%' }}
                >
                    <VideoConference />
                </LiveKitRoom>
            )}
        </div>
    );
}

export default VideoCall;
