import asyncio
import websockets
import json

connected_clients = set()

async def websocket_handler(websocket, path):
    """Handle WebSocket connections."""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Optionally handle messages from clients if needed
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    finally:
        connected_clients.remove(websocket)

async def broadcast(data):
    """Send data to all connected clients."""
    if connected_clients:  # Check if there are any connected clients
        message = json.dumps(data)
        await asyncio.wait([client.send(message) for client in connected_clients])

async def main():
    """Start the WebSocket server."""
    print("Starting WebSocket server on ws://localhost:8765")
    async with websockets.serve(websocket_handler, "localhost", 8765):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
