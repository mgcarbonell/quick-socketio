# almost identical to our regular client.py
# the only difference is we're going to remove
# sys, and make a few syntax changes:
# we will add async to our defs
# and await where we need it.

# note that these clients will work in the CLI.
import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
  print('connected')
  result = await sio.call('sum', {'numbers': [1, 2]})
  print(result)

@sio.event
async def connect_error(e):
  print(e)

@sio.event
async def disconnect():
  print('disconnected')

@sio.event
async def mult(data):
  return data['numbers'][0] * data['numbers'][1]

@sio.event
async def client_count(count):
  print('There are', count, 'connected clients.')

@sio.event
async def room_count(count):
  print('There are', count, 'clients in my room.')

@sio.event:
async def user_joined(username)
  print('User', username, 'has joined.')

@sio.event
async def user_left(username)
  print('User', username, 'has left.')

async def main(username):
  await sio.connect('http://localhost:8000',
                    headers={'X-Username': username})
  await sio.wait()
  # sio.wait will wait until the connect ends.
