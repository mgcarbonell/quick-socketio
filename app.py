# Polling, not true websockets unless we use eventlet. To use 
# eventlet, we need a gunicorn worker for eventlet.

# to startup w/ eventlet: gunicorn -k eventlet -w 1 --reload app:app
# '-k eventlet' means we want gunicorn to use eventlet (not WSGI)
# '-w' is the number of workers, right now we need 1.
# '--reload' means that whenever the code is changed, we reload.
# 'app:app' tells gunicorn to look for app and make it the server app. 

# We can have multiple workers, but that's more complex, 
# 1 worker can still handle a ton connections. 
# How to use more is in the python-socketio documentation.

import random
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
  '/': './public/'
})

client_count = 0
a_count = 0
b_count = 0


def task(sid):
  sio.sleep(5)
  result = sio.call('mult', {'numbers': [3, 4]}, to=sid)
  print(result)

# we're going to do a cheap user system by allowing a user
# to create a username by entering it localhost:8000/#username
# we will write this to the user session.
@sio.event
def connect(sid, environ):
  global client_count
  global a_count
  global b_count

  username = environ.get('HTTP_X_USERNAME')
  print('username: ', username)
  if not username:
    return False

  with sio.session(sid) as session: #this is a dictionary. We
    session['username'] = username  #can write directly to it.
  sio.emit('user_joined', username) #We can emit to test it.

  client_count += 1
  print(sid, 'connected')
  sio.start_background_task(task, sid)
  sio.emit('client_count', client_count)
  if random.random() > 0.5:
      sio.enter_room(sid, 'a')
      a_count += 1
      sio.emit('room_count', a_count, to='a')
  else:
      sio.enter_room(sid, 'b')
      b_count += 1
      sio.emit('room_count', b_count, to='b')


@sio.event
def disconnect(sid):
  global client_count
  global a_count
  global b_count
  client_count -= 1
  print(sid, 'disconnected')
  sio.emit('client_count', client_count)
  if 'a' in sio.rooms(sid):
      a_count -= 1
      sio.emit('room_count', a_count, to='a')
  else:
      b_count -= 1
      sio.emit('room_count', b_count, to='b')
  
  with sio.session(sid) as session:
    sio.emit('user_left', session['username'])

@sio.event
def sum(sid, data):
  result = data['numbers'][0] + data['numbers'][1]
  return {'result': result}

  