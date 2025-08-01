const initializeSocketIO = (io , {PressurePoints}) => {
    console.log("socket");

    io.on("connection", (socket) => {
        console.log(`Client Connected: ${socket.id}`);





        socket.on("disconnect", () => {
            console.log(`Client Disconnected: ${socket.id}`);
        });
    });
};

module.exports = initializeSocketIO;
