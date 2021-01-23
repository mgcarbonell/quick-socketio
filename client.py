import asyncio
import sys
import socketio

sio = socket.ioClient()

@sio.event
def connect():
  print('connected')
  result = sio.call('sum', {'numbers': [1, 2]})
  print(result)

@sio.event
def connect_error(e):
  print(e)

@sio.event
def disconnect():
  print('disconnected')