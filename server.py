import asyncio
import websockets
import os


async def consumer_handler(websocket):
    async for message in websocket:
        print(f"<< {message}")


async def producer_handler(websocket):
    directory = './for_client/'
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            with open(f'{directory}{filename}', mode='r', encoding='utf-8') as f:
                message = f.read()
                if message:
                    await websocket.send(message)
                    print(f">> {message}")
            os.replace(f'{directory}{filename}', f'{directory}success/{filename}')
        else:
            continue


async def handler(websocket, path):
    while True:
        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket))
        producer_task = asyncio.ensure_future(
            producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
