# similar to our serer, with some minor
# differences. Rather than socket.ioServer
# we use socket.ioClient.

# we still have code that is event driven,
# and this is important with socketio.

# Rather than using cb's in JS, we can use
# call in socket.ioClient().

# note that these clients will work in the CLI.

import asyncio
import sys
import socketio

sio = socketio.Client()

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

@sio.event
def mult(data):
  return data['numbers'][0] * data['numbers'][1]

@sio.event
def client_count(count):
  print('There are', count, 'connected clients.')

@sio.event
def room_count(count):
  print('There are', count, 'clients in my room.')

@sio.event:
def user_joined(username)
  print('User', username, 'has joined.')

@sio.event
def user_left(username)
  print('User', username, 'has left.')

def main(username):
  sio.connect('http://localhost:8000',
              headers={'X-Username': username})
  sio.wait()
  # sio.wait will wait until the connect ends.

if __name__ == '__main__'
  main(sys.argv[1] if lens(sys.argv) > 1 else None)
  # take 1st argument from command line if available
  # set it to none. Test for rejected connection.