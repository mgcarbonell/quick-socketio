# Note, we need to use uvicorn for websocket support.
# to startup: uvicorn --reload async_app:app
import socketio

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio, static_files={
  '/': './public/'
})

@sio.event
async def connect(sid, environ):
  print(sid, 'connected')

@sio.event
async def disconnect(sid):
  print(sid, 'disconnected')

@sio.event
async def sum(sid, data):
  result = data['numbers'][0] + data['numbers'][1]
  await sio.emit('sum_result', {'result': result}, to=sid)

