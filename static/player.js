var board = null
var game = new Chess()
toastr.options.closeButton = true;
// toastr.options.closeDuration  = 500;
// toastr.options.showDuration  = 1;
const orientation = $('input[name=orientation]').val();
const username = $('input[name=username]').val();
var opponent__username = $('input[name=opponent_username]').val();


function onDragStart(source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.game_over()) return false


    // only pick up pieces for the side to move

    if (orientation === 'white') {

        if (game.turn() === 'b') {
            return false
        }
    } else {
        if (game.turn() === 'w') {
            return false
        }
    }

    // console.log(game.turn())
    // if ((game.turn() === 'w' && piece.search(/^b/) !== -1) || (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    //     return false
    // }
}

function onDrop(source, target) {
    // see if the move is legal

    var move = game.move({
        from: source,
        to: target,
        promotion: 'q' // NOTE: always promote to a queen for example simplicity
    })


    // illegal move
    if (move === null) return 'snapback'


    socket.emit('broad_cast_fen', {
        fen: game.fen(),
        move: move,
        room: room
    });

    updateStatus()
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd() {
    board.position(game.fen())
}

function updateStatus() {
    var status = ''

    var moveColor = 'white'
    if (game.turn() === 'b') {
        moveColor = 'black'
    }

    // checkmate?
    if (game.in_checkmate()) {
        var winner = username

        if (moveColor === orientation) {
            winner = opponent__username
        }

        socket.emit('checkmate', {
            room: room,
            winner: winner
        });
    }

    // draw?
    else if (game.in_draw()) {

    }

    // game still on
    else {

        // check?
        if (game.in_check()) {
            socket.emit('check', {
                room: room,
                color: moveColor
            });
        }
    }
}

var config = {
    draggable: true,
    position: 'start',
    orientation: orientation,
    onDragStart: onDragStart,
    onDrop: onDrop,
    onSnapEnd: onSnapEnd
}
board = Chessboard('board1', config)

updateStatus()
const room = $('input[name=room]').val();
const fen = $('input[name=fen]').val();


if (fen) {
    board.position(fen)
    game.load(fen)
}


$.ajaxSetup({
    headers: {
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
    }
});

socket.emit('login', {room: room, username: username});

socket.on('receive_fen', function (data) {
    board.position(data.fen);
    game.load(data.fen);
    printMoves(JSON.parse(data.moves));


});

socket.on('in_check', function (data) {
    if (data.color === orientation) {
        toastr.error('check', 'Attention')
    }
})
socket.on('game_finished', function (data) {
    data = JSON.parse(data)
    if (data.winner === username) {
        toastr.success('checkmate', 'WIN')

    } else {
        toastr.error('checkmate', 'LOST')
    }

})

socket.on('user:on', function (data) {
    if (data.length === 2) {
        $('.opponent').find('.status').removeClass('offline__status')
        $('.opponent').find('.status').addClass('online__status')
        opponent__username = data.username
        $('.opponent').find('.opponent__username').text(opponent__username)
    }
})


socket.on('user:off', function (data) {
    $('.opponent').find('.status').removeClass('online__status');
    $('.opponent').find('.status').addClass('offline__status');
})


function printMoves(moves) {
    let html = '';

    $.each(moves, function (i, m) {
        html += '<span class="move">' + (i + 1) + ' ' + m + '</span>';
    })

    $('#moves__div').html(html);
}

$('#surrender__btn').click(function () {
    if (confirm('Are you sure?')) {
        socket.emit('checkmate', {
            room: room,
            winner: opponent__username
        });
    }
})