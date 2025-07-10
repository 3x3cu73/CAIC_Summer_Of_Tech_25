const {AccessToken} = require("livekit-server-sdk");
const initializeSocketIO = (io) => {
    console.log("socket");
    io.on("connection", (socket) => {
        console.log(`Client Connected: ${socket.id}`);


        socket.on('setup', (userId) => {
            socket.join(userId);
            socket.emit('connected');
            console.log(`User ${userId} joined personal room.`);
        });


        socket.on('joinChat', (chatId) => {
            socket.join(chatId);
            console.log(`User ${socket.id} joined chat room: ${chatId}`);
        });


        socket.on('newMessage', (messageData) => {
            const { chatId, message, sender } = messageData;


            socket.to(chatId).emit('messageReceived', {
                message,
                sender,
                timestamp: new Date()
            });

            console.log(`Message sent in chat ${chatId} by ${sender.name}`);
        });


        socket.on('typing', (data) => {
            const { chatId, user } = data;
            socket.to(chatId).emit('typing', { user, chatId });
        });

        socket.on('stopTyping', (data) => {
            const { chatId, user } = data;
            socket.to(chatId).emit('stopTyping', { user, chatId });
        });


        const { AccessToken } = require('livekit-server-sdk');

        socket.on('join-video-room', async (data, callback) => {
            const { roomId, roomName, creator } = data;

            console.log(`User ${creator} is requesting to join video room: ${roomName}`);

            try {
                // Create new access token with API key/secret and user identity
                let token = new AccessToken(
                    process.env.LIVEKIT_API_KEY,
                    process.env.LIVEKIT_API_SECRET,
                    {
                        identity: creator,
                        ttl: '1h',
                    }
                );

                // Add room-level grant to the token
                token.addGrant({
                    roomJoin: true,
                    room: `${roomName}_${roomId}`,
                    canPublish: true,
                    canSubscribe: true,
                });


                const jwt = await token.toJwt();

                // Respond to the client using the callback
                callback({ success: true, token: jwt });
            } catch (error) {
                console.error("Error generating Video Token", error);
                callback({ success: false, message: "Could not generate token." });
            }
        });


        socket.on("disconnect", () => {
            console.log(`Client Disconnected: ${socket.id}`);
        });
    });
};

module.exports = initializeSocketIO;
