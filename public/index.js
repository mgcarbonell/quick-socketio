// setting customer headers for "user auth"
// we're going to do a cheap user system by allowing a user
// to create a username by entering it localhost:8000/#username
const sio = io({
  transportOptions: {
    polling: {
      extraHeaders: {
        'X-Username': window.location.hash.substring(1)
      }
    }
  }
});

sio.on('connect', () => {
  console.log('connected');
  sio.emit('sum', {numbers: [1, 2]}, (result) => {
    console.log(result);
  });
});

sio.on('connect_error', (e) => {
  console.log(e.message);
});

sio.on('disconnect', () => {
  console.log('disconnected');
});

sio.on('mult', (data, cb) => {
  const result = data.numbers[0] * data.numbers[1];
  cb(result);
});

sio.on('client_count', (count) => {
  console.log(`There are ${count} connected clients.`);
});

sio.on('room_count', (count) => {
  console.log(`There are ${count} clients in my room.`);
});

sio.on('user_joined', (username) => {
  console.log(`User ${username} has joined.`);
});

sio.on('user_left', (username) => {
  console.log(`User ${username} has left.`);
});


// note: this function was replaced by adding a THIRD
// argument to our connect sio emit function. That
// third argument is a CALLBACK FUNCTION with result
// as its argument. What happens here is when the
// client connects, the information is sent, and the
// callback waits for the results to then log it.

// sio.on('sum_result', (data) => {
//   console.log(data);
// });