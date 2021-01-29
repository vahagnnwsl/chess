var board = null
var game = new Chess()
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')
const orientation = $('input[name=orientation]').val();

function onDragStart(source, piece, position, orientation) {
    // do not pick up pieces if the game is over
    if (game.game_over()) return false

    let a, b;

    if (orientation === 'white') {
        a = 'w';
        b = 'b';
    } else {
        a = 'b';
        b = 'w';
    }

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

    var moveColor = 'White'
    if (game.turn() === 'b') {
        moveColor = 'Black'
    }

    // checkmate?
    if (game.in_checkmate()) {
        status = 'Game over, ' + moveColor + ' is in checkmate.'
        alert(status)

    }

    // draw?
    else if (game.in_draw()) {
        status = 'Game over, drawn position'
    }

    // game still on
    else {
        status = moveColor + ' to move'

        // check?
        if (game.in_check()) {
            status += ', ' + moveColor + ' is in check'
            alert(status)

        }
    }

    $status.html(status)
    $fen.html(game.fen())
    $pgn.html(game.pgn())
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

var socket = io('http://127.0.0.1:3000');

socket.emit('login', room);

$.ajaxSetup({
    headers: {
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
    }
});


socket.on('receive_fen', function (data) {
    board.position(data.fen)
    game.load(data.fen)
    $.ajax({
        url: `/room/${room}/fen`,
        method: 'POST',
        data: {
            fen: data.fen
        },
        success: function () {

        }
    })
});


