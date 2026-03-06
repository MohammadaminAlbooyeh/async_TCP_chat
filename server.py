import asyncio

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.clients = []

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")
        self.clients.append(writer)

        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break

                message = data.decode().strip()
                print(f"Received message from {addr}: {message}")

                # Broadcast the message to all other clients
                await self.broadcast(message, writer)
        except asyncio.CancelledError:
            pass
        finally:
            print(f"Connection closed from {addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                try:
                    client.write(f"{message}\n".encode())
                    await client.drain()
                except Exception as e:
                    print(f"Error sending message: {e}")

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"Server started on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    chat_server = ChatServer()
    try:
        asyncio.run(chat_server.start_server())
    except KeyboardInterrupt:
        print("Server shut down.")