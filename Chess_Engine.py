
class Game_State():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (0, 4)
        self.blackKingLocation = (7, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)

        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = (int((move.startRow + move.endRow) / 2), move.startCol)

        else:
            self.enpassantPossible = ()

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = "--"
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                 self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)

            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow):
                self.enpassantPossible = ()

            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs,)

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"




    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False

        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False



    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                        self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves


    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r ,c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False



    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == "p":
                        self.getPawnMoves(r, c, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enpassantPossible=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enpassantPossible=True))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, enpassantPossible=True))

            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enpassantPossible=True))


    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            T = "b"
        else:
            T = "w"

        if r != 0:
            for row in range(r-1,-1,-1):
                if self.board[row][c] != "--":
                    if self.board[row][c][0] == T:
                        moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, c), self.board))
        if r != 7:
            for row in range(r+1, 8):
                if self.board[row][c] != "--":
                    if self.board[row][c][0] == T:
                        moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, c), self.board))
        if c != 0:
            for col in range(c-1,-1,-1):
                if self.board[r][col] != "--":
                    if self.board[r][col][0] == T:
                        moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    moves.append(Move((r, c), (r, col), self.board))
        if c != 7:
            for col in range(c+1, 8):
                if self.board[r][col] != "--":
                    if self.board[r][col][0] == T:
                        moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    moves.append(Move((r, c), (r, col), self.board))

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            T = "b"
        else:
            T = "w"

        colr1 = c
        if r != 0 and c != 7:
            for row in range(r-1,-1,-1):
                colr1 += 1
                if colr1 == 8:
                    break
                if self.board[row][colr1] != "--":
                    if self.board[row][colr1][0] == T:
                        moves.append(Move((r, c), (row, colr1), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, colr1), self.board))

        colle = c
        if r != 0 and c != 0:
            for row in range(r-1,-1,-1):
                colle -= 1
                if colle == -1:
                    break
                if self.board[row][colle] != "--":
                    if self.board[row][colle][0] == T:
                        moves.append(Move((r, c), (row, colle), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, colle), self.board))

        colr2 = c
        if r != 7 and c != 7:
            for row in range(r+1, 8):
                colr2 += 1
                if colr2 == 8:
                    break
                if self.board[row][colr2] != "--":
                    if self.board[row][colr2][0] == T:
                        moves.append(Move((r, c), (row, colr2), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, colr2), self.board))

        colle2 = c
        if r != 7 and c != 0:
            for row in range(r+1,8):
                colle2 -= 1
                if colle2 == -1:
                    break
                if self.board[row][colle2] != "--":
                    if self.board[row][colle2][0] == T:
                        moves.append(Move((r, c), (row, colle2), self.board))
                    break
                else:
                    moves.append(Move((r, c), (row, colle2), self.board))

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            T = "b"
        else:
            T = "w"

        if r != 0:
            if self.board[r-1][c] != "--":
                if self.board[r-1][c][0] == T:
                    moves.append(Move((r, c), (r-1, c), self.board))
            else:
                moves.append(Move((r, c), (r - 1, c), self.board))

        if r != 7:
            if self.board[r+1][c] != "--":
                if self.board[r+1][c][0] == T:
                    moves.append(Move((r, c), (r+1, c), self.board))
            else:
                moves.append(Move((r, c), (r + 1, c), self.board))

        if c != 0:
            if self.board[r][c - 1] != "--":
                if self.board[r][c-1][0] == T:
                    moves.append(Move((r, c), (r, c-1), self.board))
            else:
                moves.append(Move((r, c), (r, c-1), self.board))

        if c != 7:
            if self.board[r][c + 1] != "--":
                if self.board[r][c+1][0] == T:
                    moves.append(Move((r, c), (r, c+1), self.board))
            else:
                moves.append(Move((r, c), (r, c+1), self.board))

        if r != 0 and c != 7:
            if self.board[r - 1][c + 1] != "--":
                if self.board[r - 1][c + 1][0] == T:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            else:
                moves.append(Move((r, c), (r - 1, c + 1), self.board))

        if r != 0 and c != 0:
            if self.board[r - 1][c - 1] != "--":
                if self.board[r - 1][c - 1][0] == T:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            else:
                moves.append(Move((r, c), (r - 1, c - 1), self.board))

        if r != 7 and c != 0:
            if self.board[r + 1][c - 1] != "--":
                if self.board[r + 1][c - 1][0] == T:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            else:
                moves.append(Move((r, c), (r + 1, c - 1), self.board))

        if r != 7 and c != 7:
            if self.board[r + 1][c + 1] != "--":
                if self.board[r + 1][c + 1][0] == T:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
            else:
                moves.append(Move((r, c), (r + 1, c + 1), self.board))



    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            T = "b"
        else:
            T = "w"

        if r - 2 >= 0 and c + 1 <= 7:
            if self.board[r-2][c+1] != "--":
                if self.board[r-2][c+1][0] == T:
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
            else:
                moves.append(Move((r, c), (r - 2, c + 1), self.board))

        if r - 2 >= 0 and c - 1 >= 0:
            if self.board[r-2][c-1] != "--":
                if self.board[r-2][c-1][0] == T:
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
            else:
                moves.append(Move((r, c), (r - 2, c - 1), self.board))

        if r + 2 <= 7 and c + 1 <= 7:
            if self.board[r+2][c+1] != "--":
                if self.board[r+2][c+1][0] == T:
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
            else:
                moves.append(Move((r, c), (r + 2, c + 1), self.board))

        if r + 2 <= 7  and c - 1 >= 0:
            if self.board[r+2][c-1] != "--":
                if self.board[r+2][c-1][0] == T:
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
            else:
                moves.append(Move((r, c), (r + 2, c - 1), self.board))

        if r - 1 >= 0 and c + 2 <= 7:
            if self.board[r-1][c+2] != "--":
                if self.board[r-1][c+2][0] == T:
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            else:
                moves.append(Move((r, c), (r - 1, c + 2), self.board))

        if r + 1 <= 7 and c + 2 <= 7:
            if self.board[r+1][c+2] != "--":
                if self.board[r+1][c+2][0] == T:
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            else:
                moves.append(Move((r, c), (r + 1, c + 2), self.board))

        if r + 1 <= 7 and c - 2 >= 0:
            if self.board[r+1][c-2] != "--":
                if self.board[r+1][c-2][0] == T:
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
            else:
                moves.append(Move((r, c), (r + 1, c - 2), self.board))

        if r - 1 >= 0 and c - 2 >= 0:
            if self.board[r-1][c-2] != "--":
                if self.board[r-1][c-2][0] == T:
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            else:
                moves.append(Move((r, c), (r - 1, c - 2), self.board))


    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))


    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3]:
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))





class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs




class Move():

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enpassantPossible = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            if self.pieceMoved == "bp":
                self.pieceCaptured = "wp"
            else:
                self.pieceCaptured = "bp"
        self.isCastleMove = isCastleMove
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol



    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]