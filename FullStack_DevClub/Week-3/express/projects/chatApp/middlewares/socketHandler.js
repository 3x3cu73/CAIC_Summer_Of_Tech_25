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


        socket.on("disconnect", () => {
            console.log(`Client Disconnected: ${socket.id}`);
        });
    });
};

module.exports = initializeSocketIO;
