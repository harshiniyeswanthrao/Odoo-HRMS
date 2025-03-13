const WebSocket = require('ws');
const http = require('http');

// Create an HTTP server
const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('WebSocket server is running');
});

// Create a WebSocket server attached to the HTTP server
const wss = new WebSocket.Server({
    server: server, // Associate WebSocket with HTTP server
    clientTracking: true,
    // Enable per-origin CORS support
    verifyClient: (info, callback) => {
        const origin = info.origin;
        if (origin === 'http://localhost:8068') {  // Allow CORS for this origin
            callback(true);
        } else {
            callback(false, 403, 'Forbidden');
        }
    }
});

wss.on('connection', socket => {
    console.log('Client connected');

    socket.on('message', message => {
        console.log('Message received:', message);
        // Example: Echo message back to client
        socket.send(`Server received: ${message}`);
    });

    socket.on('close', () => {
        console.log('Client disconnected');
    });
});

// Start the HTTP server on port 3000
server.listen(3000, () => {
    console.log('WebSocket server is running on ws://localhost:3000');
});
