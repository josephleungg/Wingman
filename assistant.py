import asyncio
import socketio
import os

sio = socketio.AsyncClient()

async def socket_connect():
    await sio.connect('http://192.168.0.127:5000', transports=['polling'])
    await sio.wait()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
async def message(data):
  print("Received:",data)
  os.system(f"espeak '{data}'")

asyncio.run(socket_connect())