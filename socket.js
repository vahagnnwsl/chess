const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);

app.get('/', (req, res) => {
    res.json({a: 1});
});

io.on('connection', function (socket) {

    socket.on('broad_cast_fen', function (data) {
        io.sockets.in(data.room).emit('receive_fen', data);
    });
    socket.on('login', function (room) {

        io.sockets.in(room).emit('user:on', {room: room, length: io.sockets.adapter.rooms.get(room).size});
    });
    socket.on('idle', function () {
        Object.keys(io.sockets.adapter.rooms).forEach(function (room) {
            if (io.sockets.adapter.rooms[room].length > 1) {
                socket.broadcast.to(room).emit('user:away', room);
            }
        });
    });
    socket.on('active', function () {

        Object.keys(io.sockets.adapter.rooms).forEach(function (room) {
            socket.broadcast.to(room).emit('user:on', {room: room, length: io.sockets.adapter.rooms[room].length});
        });
    });
    socket.on('disconnect', function () {
        console.log('disconnect')
        Object.keys(io.sockets.adapter.rooms).forEach(function (room) {
            socket.broadcast.to(room).emit('user:off', room);
        });
    });

});


http.listen(3000, () => {
    console.log('listening on *:3000');
});