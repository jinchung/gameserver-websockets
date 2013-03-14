""" Game Server """

import socket
import game
import random
import messages as m
import json

games_in_play = {}
games_pending = {}
server = None

games_pending["tictactoe"] = []
games_pending["connect4"] = []
games_pending["chess"] = []
games_pending["checkers"] = []
games_pending["go"] = []

def setServerHandler(serverHandler):
    global server
    server = serverHandler

def handleIncomingMsg(data, sid):
    try:
        inputMsg = m.parse(data)
        type = inputMsg.type
    except :
        type = 'error'
    if type == "new":
        handleJoinGame(inputMsg, sid)    
    elif type == "move":
        handleMove(inputMsg, sid)
    else:
        msg = 'Error reading game request. Please make sure message type is either [new] or [move]'
        error = m.ResponseMessage('error', None, None, None, msg, False)
        print 'Error reading game request.'
        sendMessage(sid, error)

def movePendingToPlay(g, sid):
    games_in_play[g.id] = g
    g.players.append(sid)
    announcenew =  m.ResponseMessage("new", g.id, g.type, None, "Game is now live", False)
    sendMessage(sid, announcenew)
    sendMessage(g.players[0], announcenew)
    randomlyChooseFirstPlayerAndStartGame(g)

def sendMessage(sid, msg):
    jsonToSend = json.dumps(msg.__dict__)
    server.sendMessage(sid, jsonToSend)

def randomlyChooseFirstPlayerAndStartGame(g):
    g.currPlayerIndex = random.randint(0,1)
    print 'randomly choose first player: ', g.currPlayerIndex
    constructGamePlayMsg(g)

def constructGamePlayMsg(g):
    print 'constructing the play game msg', g.getCurrMarker(), g.currPlayerIndex
    play = m.ResponseMessage("play", g.id, g.type, g.gamestate, "Play", True, None, g.getCurrMarker(), g.getOppMarker())
    sendMessage(g.getCurrPlayer(), play)

def createNewGame(inputMsg, sid):
    g = game.buildNewGame(inputMsg.gameType, sid)
    games_pending[g.type].append(g)
    announce = m.ResponseMessage("announce", None, g.type, None, "Created a new game. Please wait for another player to connect.", False)
    sendMessage(sid, announce)

def handleJoinGame(inputMsg, sid):
    print 'User has requested to join any game of type: %s' % (inputMsg.gameType)
    possGames = games_pending[inputMsg.gameType]
    if possGames:
        print 'Game of type %s exists. Joining game now.' % (inputMsg.gameType)
        movePendingToPlay(possGames.pop(0), sid)
    else:
        print 'Game of type %s does not exist yet. Creating a new game.' % (inputMsg.gameType)
        createNewGame(inputMsg, sid)

def handleMove(inputMsg, sid):
    if inputMsg.gameId in games_in_play:
        g = games_in_play[inputMsg.gameId]
        success, msg, hasWinner, isTied = g.move(inputMsg.move, sid)
        if success:
            if hasWinner:
                winMsg = m.ResponseMessage('gameover', g.id, g.type, g.gamestate, 'You have won.', False, inputMsg.move, g.getCurrMarker(), g.getOppMarker())
                loseMsg = m.ResponseMessage('gameover', g.id, g.type, g.gamestate, 'You have lost.', False, inputMsg.move, g.getCurrMarker(), g.getOppMarker())
                sendMessage(g.getCurrPlayer(), loseMsg)
                sendMessage(g.getOtherPlayer(), winMsg)
                gameCleanup(g)
            else:
                if isTied:
                    tiedMsg = m.ResponseMessage('gameover', g.id, g.type, g.gamestate, 'Game is tied.', False, inputMsg.move, g.getCurrMarker(), g.getOppMarker())
                    sendMessage(g.getCurrPlayer(), tiedMsg)
                    sendMessage(g.getOtherPlayer(), tiedMsg)
                    gameCleanup(g)
                else:
                    announce = m.ResponseMessage('announce', g.id, g.type, g.gamestate, 'Success.', False)
                    play = m.ResponseMessage('play', g.id, g.type, g.gamestate, 'Play', True, inputMsg.move, g.getCurrMarker(), g.getOppMarker())
                    sendMessage(g.getCurrPlayer(), play)
                    sendMessage(g.getOtherPlayer(), announce)
        else:
            error = m.ResponseMessage('error', g.id, g.type, g.gamestate, msg, True)
            sendMessage(sid, error)
    else:
        error = m.ResponseMessage('error', None, None, None, 'Cannot find game with that ID', False)
        sendMessage(sid,error)

def gameCleanup(g):
    del games_in_play[g.id]
