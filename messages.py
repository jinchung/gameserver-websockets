""" 
Functions and classes for message parsing 
"""
import ast
    
class RequestMessage(object):
    def __init__(self, type, gameId, gameType, move):
        self.type = type
        self.gameId = gameId
        self.gameType = gameType
        self.move = move
        
class ResponseMessage(object):
    def __init__(self, type, gameId, gameType, gamestate, msg, isCurrPlayer, lastMove=None, currMarker=None, oppMarker=None):
        self.type = type
        self.gameId = gameId
        self.gameType = gameType
        self.gamestate = gamestate
        self.msg = msg
        self.isCurrPlayer = isCurrPlayer
        self.currMarker = currMarker
        self.oppMarker = oppMarker
        self.lastMove = lastMove

def parse(data):
    dataDict = ast.literal_eval(data)
    return RequestMessage(dataDict["type"], dataDict["gameId"], dataDict["gameType"], dataDict["move"])
