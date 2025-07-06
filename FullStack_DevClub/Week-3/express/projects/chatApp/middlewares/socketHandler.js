const initializeSocketIO = (io) => {

    io.on("connection", (socket) => {
        console.log(`✅ Client Connected: ${socket.id}`);

        // Event for a user to join their personal notification room
        socket.on('setup', (userId) => {
            socket.join(userId);
            socket.emit('connected');
            console.log(`User ${userId} joined personal room.`);
        });

        // Event for a user to join a specific chat room
        socket.on('joinChat', (chatId) => {
            socket.join(chatId);
            console.log(`User ${socket.id} joined chat room: ${chatId}`);
        });


        // Event for when a client disconnects
        socket.on("disconnect", () => {
            console.log(`❌ Client Disconnected: ${socket.id}`);
        });
    });
};

module.exports = initializeSocketIO;
