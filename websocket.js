var gameType;
var currMarker;
var oppMarker;
var gameId; 
var isCurrPlayer = false;
var ws = null; 

$(document).ready(function () {

    $("#gamestart").click(function(evt) {
        evt.preventDefault();
        var gameTypeResults = document.getElementsByName("gameType");
        for (var i=0; i < gameTypeResults.length; i++){
            if (gameTypeResults[i].checked){
                gameType = gameTypeResults[i].id;
            }   
        }
        newgamereq = "{'type': 'new', 'gameId': None, 'gameType': '" + gameType + "', 'move': None}";
        if (ws == null) {
            alert('creating a new web socket');
            createWebsocket(newgamereq);
        } else {
            alert('reusing websocket for new game');
            ws.send(newgamereq);
        }
    });

});


function createWebsocket(newgamereq){
    ws = new WebSocket("ws://localhost:8888/gameserver"); 
    ws.onopen = function() {ws.send(newgamereq);};
    ws.onmessage = function(evt) {
        var gameMsg = JSON.parse(evt.data);
        document.getElementById("announcements").innerHTML = gameMsg.msg;
        switch(gameMsg.type){
            case "new":
                gameId = gameMsg.gameId;
                drawBoard(3); 
                break;
            case "play":
                currMarker = gameMsg.currMarker;
                oppMarker = gameMsg.oppMarker;
                updateBoard(gameMsg.lastMove);
                break;
            case "announce":
                break;
            case "gameover":
                currMarker = gameMsg.currMarker;
                oppMarker = gameMsg.oppMarker;
                updateBoard(gameMsg.lastMove);
                ws.close();
                break;
            case "error":
                break;
        }
    };
}

function drawBoard(size){
    board=document.getElementById("board")
    table=document.createElement("table");
    board.appendChild(table);

    for (var r=0; r<size; r++){
        var row = table.insertRow(r);
        for (var c=0; c<size; c++){
            var col = row.insertCell(c);
            var b = document.createElement("button");
            b.id = r + " " + c;
            b.className = "t3button";
            b.onclick=function(){selectButton(this);};
            col.appendChild(b);
        }
    }
}

function selectButton(b){
    if (isCurrPlayer){
        moveMsg = "{'type': 'move', 'gameId': " + gameId + ", 'gameType': '" + gameType + "', 'move': '" + b.id + "'}";
        ws.send(moveMsg);
        b.innerHTML=currMarker;
        b.disabled=true;
        isCurrPlayer = false;
    }
    else {
        alert('SIMMA DOWN. ur foe is being slow.');
    }
}

function updateBoard(move){
    if (move != null){
        b = document.getElementById(move);
        b.innerHTML=oppMarker;
        b.disabled = true;
    }
    isCurrPlayer = true;
}


