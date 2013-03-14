var ws = null; 
var allGames = new AllGames();

$(document).ready(function () {

    $("#gamestart").click(function(evt) {
        evt.preventDefault();
        var gameTypeResults = document.getElementsByName("gameType");
        var gameType;
        for (var i=0; i < gameTypeResults.length; i++){
            if (gameTypeResults[i].checked){
                gameType = gameTypeResults[i].id;
            }   
        }
        newgamereq = "{'type': 'new', 'gameId': None, 'gameType': '" + gameType + "', 'move': None}";
        if (ws == null) {
            createWebsocket(newgamereq);
        } else {
            ws.send(newgamereq);
        }
    });

});

function AllGames(){
}

function Game(gameId, gameType, currMarker, oppMarker, isCurrPlayer){
    this.gameId = gameId;
    this.gameType = gameType;
    this.currMarker = currMarker;
    this.oppMarker = oppMarker;
    this.isCurrPlayer = isCurrPlayer;
}

function createWebsocket(newgamereq){
    ws = new WebSocket("ws://10.5.97.18:8888/gameserver"); 
    ws.onopen = function() {ws.send(newgamereq);};
    ws.onmessage = function(evt) {
        var gameMsg = JSON.parse(evt.data);
        switch(gameMsg.type){
            case "new":
                addGameToArena(gameMsg.gameId, gameMsg.gameType); 
                break;
            case "play":
                //shouldn't have to get currMarker and oppMarker everytime - only once
                allGames[gameMsg.gameId].currMarker = gameMsg.currMarker;
                allGames[gameMsg.gameId].oppMarker = gameMsg.oppMarker;
                allGames[gameMsg.gameId].isCurrPlayer = gameMsg.isCurrPlayer;
                updateBoard(gameMsg.gameId, gameMsg.lastMove);
                break;
            case "announce":
                break;
            case "gameover":
                allGames[gameMsg.gameId].currMarker = gameMsg.currMarker;
                allGames[gameMsg.gameId].oppMarker = gameMsg.oppMarker;
                updateBoard(gameMsg.gameId, gameMsg.lastMove);
                break;
            case "error":
                break;
        }
        if (gameMsg.gameId == null){
            document.getElementById("globalMsg").innerHTML = gameMsg.msg;
        } else {
            gamePlay = document.getElementById(gameMsg.gameId);
            announce = gamePlay.getElementsByClassName("announcements")[0];
            announce.innerHTML = gameMsg.msg;
            document.getElementById("globalMsg").innerHTML = '';
        }
    };
}

function addGameToArena(gid, gameType){
    game = new Game(gid, gameType, null, null, null);
    allGames[gid] = game;
    arena=document.getElementById("arena");
    
    gamePlay=document.createElement("div");
    gamePlay.className="gamePlay";
    gamePlay.id=gid;

    announce=document.createElement("div");
    announce.className="announcements";

    board = drawBoard(gid, gameType);

    gameId=document.createElement("label");
    gameId.className="gameId";
    gameId.innerHTML="Game ID: " + gid;

    arena.innerHTML= '';
    arena.appendChild(gamePlay);
    gamePlay.appendChild(announce);
    gamePlay.appendChild(board);
    gamePlay.appendChild(gameId);
        
}

function drawBoard(gid, gameType){
    board=document.createElement("div");

    switch(gameType){
        case "tictactoe":
            drawTicTacToeBoard(gid, 3, board, gameType);
            break;
        case "go":
            drawGoBoard(gid, board);
            break;
    }
    return board;
}

function drawTicTacToeBoard(gid, size, board, gameType){
    board.className="t3board";
    table=document.createElement("table");
    board.appendChild(table);
    for (var r=0; r<size; r++){
        var row = table.insertRow(r);
        for (var c=0; c<size; c++){
            var col = row.insertCell(c);
            var b = document.createElement("button");
            b.id = r + " " + c;
            b.className = "t3button";
            b.onclick=function(){selectButton(this, gid, gameType);};
            col.appendChild(b);
        }
    }
}

function drawGoBoard(gid, board){
    board.className="goboard";
    canvas=document.createElement("canvas");
    canvas.id="goboard";
    canvas.width="500";
    canvas.height="500";
    canvas.onclick=function(evt){placeGoMarker(this, evt, gid);};
    board.appendChild(canvas);
}

function placeGoMarker(canvas, evt, gid){
    if (allGames[gid].isCurrPlayer){
        rect=canvas.getBoundingClientRect();
        x=evt.clientX - rect.left;
        y=evt.clientY - rect.top;
        ctx=canvas.getContext("2d"); 
        ctx.beginPath();
        ctx.arc(x, y, 10, 0, 2 * Math.PI, false);
        if (allGames[gid].currMarker == 'B'){
            ctx.fillStyle="black";
        }
        else {
            ctx.fillStyle="white";
        }
        ctx.fill();
        //alert('rect left is ' + rect.left + ' rect top is ' + rect.top);
        //alert('client x is ' + evt.clientX);
        //alert('client y is ' + evt.clientY);
        move= x + ' ' + y;
        moveMsg = "{'type': 'move', 'gameId': " + gid + ", 'gameType': 'go', 'move': '" + move + "'}";
        ws.send(moveMsg);
        allGames[gid].isCurrPlayer = false;
    } 
    else {
        alert('no. simma down.');
    }
}

function selectButton(b, gid, gameType){
    if (allGames[gid].isCurrPlayer){
        moveMsg = "{'type': 'move', 'gameId': " + gid + ", 'gameType': '" + gameType + "', 'move': '" + b.id + "'}";
        ws.send(moveMsg);
        b.innerHTML=allGames[gid].currMarker;
        b.disabled=true;
        allGames[gid].isCurrPlayer = false;
    }
    else {
        alert('no. simma down.');
    }
}

function updateBoard(gid, move){
    if (move != null){
        switch (allGames[gid].gameType){
            case "tictactoe":
                updateTicTacToeBoard(gid, move);
                break;
            case "go":
                updateGoBoard(gid, move);
                break;
        }
    }
}

function updateTicTacToeBoard(gid, move){
    b = document.getElementById(move);
    b.innerHTML=allGames[gid].oppMarker;
    b.disabled = true;
    allGames[gid].isCurrPlayer = true;
}

function updateGoBoard(gid, move){
    canvas = document.getElementById("goboard");
    ctx = canvas.getContext("2d");
    //rect=canvas.getBoundingClientRect();
    mvs = move.split(" ");
    x=mvs[0]; //- rect.left;
    y=mvs[1]; ///- rect.top;
    //alert('rect left is ' + rect.left);
    //alert('rect right is ' + rect.top);
    //alert('x is ' + mvs[0]);
    //alert('y is ' + mvs[1]);
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, 2 * Math.PI, false);
    if (allGames[gid].oppMarker == 'B'){
        ctx.fillStyle="black";
    }
    else {
        ctx.fillStyle="white";
    }
    ctx.fill();
}
