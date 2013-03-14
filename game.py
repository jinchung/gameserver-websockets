""" 
Game Interface
"""

ID_GENERATOR = 0

class Game(object):

    def __init__(self, type, player):
        self.type = type
        self.id = generateNewId()
        self.players = [player]
        self.gamestate = ""
        self.currPlayerIndex = -1
        self.playerMarkers = None

    def getCurrPlayer(self):
        return self.players[self.currPlayerIndex]

    def getOtherPlayer(self):
        otherIndex = (self.currPlayerIndex + 1) % 2
        return self.players[otherIndex]

    def getCurrMarker(self):
        return self.playerMarkers[self.currPlayerIndex]

    def getOppMarker(self):
        otherIndex = (self.currPlayerIndex + 1) % 2
        return self.playerMarkers[otherIndex]
    
    def switchPlayer(self):
        self.currPlayerIndex = (self.currPlayerIndex + 1) % 2

class TicTacToe(Game):
    
    def __init__(self, type, player):
        super(TicTacToe, self).__init__(type, player)
        self.playerMarkers = ['X', 'O']
        self.board = createBoard(3)
        self.updateGamestate()      
        self.totalMoves = 9

    def move(self, move, sid):
        m = move.split()
        row = int(m[0])
        col = int(m[1])

        if self.getCurrPlayer() == sid:
            if self.board[row][col] == '_':
                self.board[row][col] = self.getCurrPlayerMarker()
                self.totalMoves -= 1
                isWinner, isTied = self.checkForWinner(row, col)
                self.switchPlayer()
                self.updateGamestate()
                return (True, 'Success', isWinner, isTied)
            else: 
                return (False, 'Invalid move', False, False)
        else:
            return (False, 'User is not current player', False, False)

    def updateGamestate(self):
        state = ''
        for row in self.board:
            for val in row:
                state+=val
            state+=':'
        self.gamestate = state
        print 'game state is: ' + state

    def checkForWinner(self, row, col):
        winner = self.checkRows(row) or self.checkCols(col) or self.checkForwardDiagonal() or self.checkBackwardDiagonal()
        tied = True if not winner and self.totalMoves == 0 else False
        return winner, tied            

    def checkRows(self, row):
        for c in range(0, 3):
            if self.board[row][c] != self.getCurrPlayerMarker():
                return False
        return True

    def checkForwardDiagonal(self):
        for i in range(0, 3):
            if self.board[i][i] != self.getCurrPlayerMarker():
                return False
        return True

    def checkBackwardDiagonal(self):
        for j in range(0, 3):
            if self.board[j][2 - j] != self.getCurrPlayerMarker():
                return False
        return True

    def getCurrPlayerMarker(self):
        return self.playerMarkers[self.currPlayerIndex]

    def checkCols(self, col):
        for r in range(0, 3):
            if self.board[r][col] != self.getCurrPlayerMarker():
                return False
        return True

class Go(Game):

    def __init__(self, type, player):
        super(Go, self).__init__(type, player)
        self.playerMarkers = ['B', 'W']
        self.board = createBoard(3)

    def move(self, move, sid):
        if self.getCurrPlayer() == sid:
            self.switchPlayer()
            return (True, 'Success', False, False)
        else:
            return (False, 'User is not current player', False, False)

def createBoard(size):
    board = []
    for i in range(0, size):
        board.append([])
        for j in range(0, size):
            board[i].append('_')
    return board

def buildNewGame(type, sid):
    if type == 'tictactoe':
        return TicTacToe(type, sid)
    else: 
        return Go(type, sid)

def generateNewId():
    global ID_GENERATOR
    ID_GENERATOR += 1
    return ID_GENERATOR     
