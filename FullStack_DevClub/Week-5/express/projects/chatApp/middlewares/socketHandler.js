const { AccessToken } = require("livekit-server-sdk");

const initializeSocketIO = (io, { Chat, Message, User }) => {
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

        socket.on('newMessage', async (messageData) => {
            const { chatId, message, senderId } = messageData;

            // Save message to DB
            const savedMessage = await Message.create({
                chat: chatId,
                sender: senderId,
                content: message
            });

            const populatedMessage = await savedMessage.populate([
                { path: 'sender', select: 'username email' },
                { path: 'chat', populate: { path: 'participants', select: 'username email' } }
            ]);

            await Chat.findByIdAndUpdate(chatId, { latestMessage: savedMessage._id });

            socket.to(chatId).emit('messageReceived', populatedMessage);
            console.log(`Message sent in chat ${chatId} by ${senderId}`);
        });

        socket.on('typing', ({ chatId, user }) => {
            socket.to(chatId).emit('typing', { user, chatId });
        });

        socket.on('stopTyping', ({ chatId, user }) => {
            socket.to(chatId).emit('stopTyping', { user, chatId });
        });

        socket.on('join-video-room', async (data, callback) => {
            const { roomId, roomName, creator } = data;

            try {
                let token = new AccessToken(
                    process.env.LIVEKIT_API_KEY,
                    process.env.LIVEKIT_API_SECRET,
                    { identity: creator, ttl: '1h' }
                );

                token.addGrant({
                    roomJoin: true,
                    room: `${roomName}_${roomId}`,
                    canPublish: true,
                    canSubscribe: true,
                });

                const jwt = await token.toJwt();
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
