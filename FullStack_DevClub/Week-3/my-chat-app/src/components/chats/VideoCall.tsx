import React, { useState, useEffect, useCallback } from 'react';
import {
    LiveKitRoom,
    VideoTrack,
    useTracks,
    useLocalParticipant,
    useRoomContext,
    useParticipants
} from '@livekit/components-react';
import { Track, RoomEvent, LocalTrackPublication } from 'livekit-client';
import { Loader2, AlertTriangle, MonitorUp, MonitorX, Mic, MicOff, Video, VideoOff, Phone } from 'lucide-react';
import { useSocket } from '../../context/socketHandler.js';
import { useUser } from '../../context/userContext.js';

const CallOverlay = ({ children }: { children: React.ReactNode }) => (
    <div className="absolute inset-0 bg-slate-800 bg-opacity-80 flex flex-col items-center justify-center text-white z-20">
        {children}
    </div>
);

const ShareScreenButton = () => {
    const { localParticipant } = useLocalParticipant();
    // State to track if screen sharing is currently active
    const [isScreenSharing, setIsScreenSharing] = useState(false);
    // State to hold the screen share track publications
    const [screenSharePublications, setScreenSharePublications] = useState<LocalTrackPublication[]>([]);

    const toggleScreenShare = useCallback(async () => {
        if (!localParticipant) return;

        // If currently screen sharing, stop it
        if (isScreenSharing) {
            // Iterate over the stored publications
            for (const publication of screenSharePublications) {
                // *** FIX: Check if the track exists before unpublishing ***
                if (publication.track) {
                    await localParticipant.unpublishTrack(publication.track);
                }
            }
            setScreenSharePublications([]);
            setIsScreenSharing(false);
        } else {
            // If not screen sharing, start it
            try {
                // Create screen tracks, including audio
                const tracks = await localParticipant.createScreenTracks({ audio: true });
                const publications = [];
                // Publish each track and store the publication
                for (const track of tracks) {
                    const publication = await localParticipant.publishTrack(track);
                    publications.push(publication);
                }
                setScreenSharePublications(publications);
                setIsScreenSharing(true);
            } catch (err) {
                console.error('Failed to start screen share:', err);
            }
        }
    }, [isScreenSharing, localParticipant, screenSharePublications]);


    return (
        <button
            onClick={toggleScreenShare}
            className={`px-3 py-2 text-sm font-medium rounded-lg flex items-center gap-2 transition-colors ${
                isScreenSharing
                    ? 'bg-red-500 hover:bg-red-600 text-white'
                    : 'bg-indigo-600 hover:bg-indigo-700 text-white'
            }`}
        >
            {isScreenSharing ? <MonitorX size={16} /> : <MonitorUp size={16} />}
            {isScreenSharing ? 'Stop Share' : 'Share Screen'}
        </button>
    );
};

const MediaControls = ({ onLeave }: { onLeave: () => void }) => {
    const { localParticipant } = useLocalParticipant();
    const { isMicrophoneEnabled, isCameraEnabled } = localParticipant;

    const toggleMic = useCallback(async () => {
        try {
            await localParticipant.setMicrophoneEnabled(!isMicrophoneEnabled);
        } catch (err) {
            console.error('Mic toggle error:', err);
        }
    }, [localParticipant, isMicrophoneEnabled]);

    const toggleCamera = useCallback(async () => {
        try {
            await localParticipant.setCameraEnabled(!isCameraEnabled);
        } catch (err) {
            console.error('Camera toggle error:', err);
        }
    }, [localParticipant, isCameraEnabled]);

    return (
        <div className="flex items-center gap-2">
            <button
                onClick={toggleMic}
                className={`p-3 rounded-full transition-colors ${
                    isMicrophoneEnabled
                        ? 'bg-slate-700 hover:bg-slate-600 text-white'
                        : 'bg-red-500 hover:bg-red-600 text-white'
                }`}
            >
                {isMicrophoneEnabled ? <Mic size={20} /> : <MicOff size={20} />}
            </button>
            <button
                onClick={toggleCamera}
                className={`p-3 rounded-full transition-colors ${
                    isCameraEnabled
                        ? 'bg-slate-700 hover:bg-slate-600 text-white'
                        : 'bg-red-500 hover:bg-red-600 text-white'
                }`}
            >
                {isCameraEnabled ? <Video size={20} /> : <VideoOff size={20} />}
            </button>
            <ShareScreenButton />
            <button
                onClick={onLeave}
                className="p-3 rounded-full bg-red-500 hover:bg-red-600 text-white transition-colors"
            >
                <Phone size={20} />
            </button>
        </div>
    );
};

const ParticipantTile = ({ trackRef }: { trackRef: any }) => {
    if (!trackRef || !trackRef.publication) {
        return null;
    }

    const isScreenShare = trackRef.source === Track.Source.ScreenShare;

    return (
        <div className="relative bg-slate-800 rounded-lg overflow-hidden h-full w-full aspect-video">
            <VideoTrack
                trackRef={trackRef}
                className="w-full h-full object-cover"
            />
            <div className="absolute bottom-2 left-2 bg-black bg-opacity-60 text-white text-xs px-2 py-1 rounded-md">
                {trackRef.participant.identity}
                {isScreenShare && ' (Screen)'}
            </div>
            {!isScreenShare && (
                <div className="absolute top-2 right-2 bg-black bg-opacity-50 p-1 rounded-full">
                    {trackRef.participant.isMicrophoneEnabled ? (
                        <Mic size={14} className="text-green-400" />
                    ) : (
                        <MicOff size={14} className="text-red-400" />
                    )}
                </div>
            )}
        </div>
    );
};


const VideoGrid = () => {
    const tracks = useTracks(
        [Track.Source.Camera, Track.Source.ScreenShare],
        { onlySubscribed: true }
    );
    const participants = useParticipants();

    const screenShareTracks = tracks.filter(
        trackRef => trackRef.source === Track.Source.ScreenShare
    );
    const cameraTracks = tracks.filter(
        trackRef => trackRef.source === Track.Source.Camera
    );

    const localCameraTrack = cameraTracks.find(track => track.participant.isLocal);
    const remoteCameraTracks = cameraTracks.filter(track => !track.participant.isLocal);
    const orderedCameraTracks = localCameraTrack ? [localCameraTrack, ...remoteCameraTracks] : remoteCameraTracks;


    if (tracks.length === 0) {
        return (
            <div className="flex items-center justify-center h-full text-white">
                <div className="text-center">
                    <VideoOff size={48} className="mx-auto mb-4 text-slate-400" />
                    <p className="text-slate-300">
                        {participants.length === 0
                            ? 'Waiting for participants...'
                            : 'No video streams available.'}
                    </p>
                </div>
            </div>
        );
    }

    if (screenShareTracks.length > 0) {
        const mainScreenShare = screenShareTracks[0];
        return (
            <div className="w-full h-full flex flex-col p-2 sm:p-4 gap-2 sm:gap-4">
                <div className="flex-grow min-h-0">
                    <ParticipantTile trackRef={mainScreenShare} />
                </div>
                {orderedCameraTracks.length > 0 && (
                    <div className="w-full h-28 sm:h-36 md:h-40 flex-shrink-0">
                        <div className="grid grid-flow-col auto-cols-[45%] sm:auto-cols-[30%] md:auto-cols-[200px] lg:auto-cols-[240px] gap-2 sm:gap-3 h-full overflow-x-auto">
                            {orderedCameraTracks.map(trackRef =>
                                trackRef.publication ? <ParticipantTile key={trackRef.publication.trackSid} trackRef={trackRef} /> : null
                            )}
                        </div>
                    </div>
                )}
            </div>
        )
    }

    return (
        <div className="w-full h-full p-2 sm:p-4">
            <div className="grid gap-2 sm:gap-4 h-full w-full items-center justify-center"
                 style={{
                     gridTemplateColumns: `repeat(auto-fit, minmax(clamp(150px, 40vw, 450px), 1fr))`,
                 }}>
                {orderedCameraTracks.map(trackRef =>
                    trackRef.publication ? <ParticipantTile key={trackRef.publication.trackSid} trackRef={trackRef} /> : null
                )}
            </div>
        </div>
    );
};


const RoomContent = ({ onLeave }: { onLeave: () => void }) => {
    const room = useRoomContext();
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        const handleConnectionChange = () => {
            setIsConnected(room.state === 'connected');
        };

        handleConnectionChange();
        room.on(RoomEvent.ConnectionStateChanged, handleConnectionChange);

        return () => {
            room.off(RoomEvent.ConnectionStateChanged, handleConnectionChange);
        };
    }, [room]);

    if (!isConnected) {
        return (
            <CallOverlay>
                <Loader2 className="w-8 h-8 animate-spin mb-4" />
                <span>Connecting to room...</span>
            </CallOverlay>
        );
    }

    return (
        <div className="relative h-full w-full">
            <VideoGrid />
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-30">
                <MediaControls onLeave={onLeave} />
            </div>
        </div>
    );
};

function VideoCall({ chat }: { chat: { _id: string; name: string } }) {
    const [token, setToken] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [publishAudio, setPublishAudio] = useState(true);
    const [publishVideo, setPublishVideo] = useState(true);
    const [showOptions, setShowOptions] = useState(true);
    const [isInCall, setIsInCall] = useState(false);
    const socket = useSocket();
    const { user } = useUser();

    const handleJoinWithOptions = useCallback(() => {
        if (!socket || !user || !chat) return;

        setShowOptions(false);
        setIsLoading(true);
        setError(null);

        socket.emit(
            'join-video-room',
            {
                roomName: chat.name,
                roomId: chat._id,
                creator: user.username
            },
            (response: { success: boolean; token?: string; message?: string }) => {
                setIsLoading(false);
                if (response.success && response.token) {
                    setToken(response.token);
                    setIsInCall(true);
                } else {
                    setError(response.message || 'Failed to get video token.');
                    setShowOptions(true);
                }
            }
        );
    }, [socket, user, chat]);

    const handleLeaveCall = useCallback(() => {
        setToken(null);
        setIsInCall(false);
        setShowOptions(true);
        setError(null);
    }, []);

    const handleRetry = useCallback(() => {
        setError(null);
        setShowOptions(true);
    }, []);

    useEffect(() => {
        if (!socket || !chat?._id || !user?._id) {
            setError("Missing required data. Please refresh and try again.");
            return;
        }

        return () => {
            if (isInCall) {
                handleLeaveCall();
            }
        };
    }, [socket, user, chat, isInCall, handleLeaveCall]);

    const serverUrl = import.meta.env.VITE_LIVEKIT_URL;
    const turnUrl = import.meta.env.VITE_TURN_URL;
    const turnUsername = import.meta.env.VITE_TURN_USERNAME;
    const turnPassword = import.meta.env.VITE_TURN_PASSWORD;

    return (
        <div className="relative h-full w-full bg-slate-900 overflow-hidden">
            {isLoading && (
                <CallOverlay>
                    <Loader2 className="w-8 h-8 animate-spin mb-4" />
                    <span>Joining video call...</span>
                </CallOverlay>
            )}

            {error && !isLoading && (
                <CallOverlay>
                    <AlertTriangle className="w-10 h-10 text-red-400 mb-4" />
                    <p className="text-red-300 mb-4 text-center px-4 max-w-md">
                        {error}
                    </p>
                    <button
                        onClick={handleRetry}
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-md transition-colors"
                    >
                        Try Again
                    </button>
                </CallOverlay>
            )}

            {showOptions && !isLoading && !error && (
                <CallOverlay>
                    <div className="bg-slate-800 p-6 rounded-lg max-w-md w-full mx-4 shadow-xl">
                        <h2 className="text-xl font-bold mb-2 text-center">Join Video Call</h2>
                        <p className="text-slate-300 mb-6 text-center">Room: {chat.name}</p>

                        <div className="space-y-4 mb-8">
                            <label className="flex items-center gap-3 cursor-pointer p-2 rounded-lg hover:bg-slate-700 transition-colors">
                                <input
                                    type="checkbox"
                                    checked={publishAudio}
                                    onChange={(e) => setPublishAudio(e.target.checked)}
                                    className="w-4 h-4 text-indigo-500 bg-slate-700 border-slate-600 rounded focus:ring-indigo-500 focus:ring-offset-slate-800"
                                />
                                <span className="flex items-center gap-2">
                                    <Mic size={16} />
                                    Enable Microphone
                                </span>
                            </label>
                            <label className="flex items-center gap-3 cursor-pointer p-2 rounded-lg hover:bg-slate-700 transition-colors">
                                <input
                                    type="checkbox"
                                    checked={publishVideo}
                                    onChange={(e) => setPublishVideo(e.target.checked)}
                                    className="w-4 h-4 text-indigo-500 bg-slate-700 border-slate-600 rounded focus:ring-indigo-500 focus:ring-offset-slate-800"
                                />
                                <span className="flex items-center gap-2">
                                    <Video size={16} />
                                    Enable Camera
                                </span>
                            </label>
                        </div>

                        <button
                            onClick={handleJoinWithOptions}
                            disabled={!socket || !user || !chat}
                            className="w-full px-4 py-2 font-semibold bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white rounded-md transition-colors"
                        >
                            Join Call
                        </button>
                    </div>
                </CallOverlay>
            )}

            {token && isInCall && serverUrl && (
                <LiveKitRoom
                    token={token}
                    serverUrl={serverUrl}
                    connectOptions={{
                        rtcConfig: (turnUrl && turnUsername && turnPassword) ? {
                            iceServers: [
                                { urls: 'stun:stun.l.google.com:19302' },
                                {
                                    urls: turnUrl,
                                    username: turnUsername,
                                    credential: turnPassword
                                }
                            ]
                        } : undefined
                    }}
                    video={publishVideo}
                    audio={publishAudio}
                    data-lk-theme="default"
                    style={{ height: '100%', width: '100%' }}
                    onDisconnected={handleLeaveCall}
                >
                    <RoomContent onLeave={handleLeaveCall} />
                </LiveKitRoom>
            )}
        </div>
    );
}

export default VideoCall;
