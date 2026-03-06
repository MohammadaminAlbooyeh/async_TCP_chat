import asyncio

class ChatClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    async def listen_for_messages(self, reader):
        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break
                print(f"\r{data.decode().strip()}\n> ", end="")
        except asyncio.CancelledError:
            pass

    async def send_messages(self, writer):
        try:
            while True:
                message = input(" > ")
                writer.write(f"{message}\n".encode())
                await writer.drain()
        except asyncio.CancelledError:
            pass

    async def run(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        print(f"Connected to chat server at {self.host}:{self.port}")

        # Create tasks for sending and receiving messages
        listen_task = asyncio.create_task(self.listen_for_messages(reader))
        send_task = asyncio.create_task(self.send_messages(writer))

        try:
            await asyncio.gather(listen_task, send_task)
        except asyncio.CancelledError:
            pass
        finally:
            print("Disconnected from server.")
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    client = ChatClient()
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("Client shut down.")