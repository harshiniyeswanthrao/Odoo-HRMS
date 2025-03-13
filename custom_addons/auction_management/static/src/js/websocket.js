const io = require('socket.io')(3000, {
    cors: {
        origin: '*',
    },
});

io.on('connection', (socket) => {
    console.log('A user connected:', socket.id);

    // Handle disconnection
    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
    });

    // Receive bid updates and broadcast them
    socket.on('new_bid', (data) => {
        console.log('New bid received:', data);
        io.emit('auction_update', data); // Broadcast the update to all connected clients
    });
});
