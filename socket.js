const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const request = require('request');

app.get('/', (req, res) => {
    res.json({a: 1});
});

io.on('connection', function (socket) {

    socket.on('broad_cast_fen', function (data) {


        request.post(`http://127.0.0.1:8000/game/room/${data.room}/fen`, {
            form: {
                fen: data.fen,
                move: JSON.stringify(data.move)
            }
        }, function (err, httpResponse, body) {
            data.moves = body
            io.sockets.in(data.room).emit('receive_fen', data);
        })
    });

    socket.on('check', function (data) {
        io.sockets.in(data.room).emit('in_check', data);
    });

    socket.on('checkmate', function (data) {

        request.post(`http://127.0.0.1:8000/game/room/${data.room}/checkmate`, {
            form: {
                winner: data.winner
            }
        }, function (err, httpResponse, body) {
            io.sockets.in(data.room).emit('game_finished', body);
        })
    });

    socket.on('login', function (data) {
        socket.join(data.room);
        io.sockets.in(data.room).emit('user:on', {
            room: data.room,
            username: data.username,
            length: io.sockets.adapter.rooms.get(data.room).size
        });
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

        io.sockets.adapter.rooms.forEach(function (socket_id, room) {
            socket.broadcast.to(room).emit('user:off', room);
        });


    });

});


http.listen(3000, () => {
    console.log('listening on *:3000');
});