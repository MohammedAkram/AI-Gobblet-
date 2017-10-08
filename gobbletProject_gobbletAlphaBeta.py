__author__ = 'rsimpson'


"""
I started with minimax code that I found here:
http://callmesaint.com/python-minimax-tutorial/
That code was written by Matthew Griffin

Then I added in code I got from here:
https://inventwithpython.com/tictactoe.py
That code was written by Al Sweigart

Then I started adding my own code
"""

from gobbletConstants import *
from gobbletMachine import *
import copy

DEPTHLIMIT = 4


class AlphaBetaMachine(Machine):
    def __init__(self, _name):
        # call constructor for parent class
        Machine.__init__(self, _name)

    def evaluationFunction(self, _board):
        """
        This function is used by minimax to evaluate a non-terminal state.

        Things to keep in mind:

        _board is an object of type Board, which is defined in gobbletMain.py

        You can modify the Board class, if you want.

        The _board object contains a list of stacks: _board.board. The last item in the stack (_board.board[-1])
        is on top.

        Your evaluation function should return a value between BIG_POSITIVE_NUMBER and BIG_NEGATIVE_NUMBER, both
        of which are defined in gobbletConstants.py

        A better evaluation function will allow you to prune more aggressively, which will allow you to increase
        the search depth limit (DEPTHLIMIT) defined at the top of this file.
        """
        currentvalue=0
        middleIndex=[5,6,9,10]                               #middle 4 index

        for x in middleIndex:                                                               #loops into middle index(5,6,9,10)
            if(len(_board.board[x])> 0 and _board.board[x][-1] in Y_PIECES):                #if statement checks to see if the top piece in the index is your bigpiece
                currentvalue +=2                                                            # add 3 to you currentvalue
            if(len(_board.board[x])> 0 and _board.board[x][-1] in X_PIECES):                #same as if statment above but checks if the piece is your opponents
                currentvalue -=2                                                            #if its your opponents piece subtract 3 from currentvalue

        squareTuples = [(5, 6, 4, 7),(5,4,6,7),(5,7,4,6),(4,6,5,7),(4,7,5,6), (6,7,4,5),
                        (5, 9, 1, 13),(5,1,9,13),(5,13,1,9),(1,9,5,13),(1,13,5,9),(9,13,5,1),
                        (5,10,0,15),(5,0,10,15),(5,15,10,0),(0,10,5,15),(0,15,5,10),(15,10,0,5),
                        (9,6,3,12),(6,3,9,12),(6,12,3,9),(3,9,6,12),(3,12,6,9),(9,12,3,6),
                        (9,10,8,11),(9,8,10,11),(9,11,10,8),(8,10,9,11),(8,11,9,10),(10,11,8,9),
                        (10,6,2,14),(10,14,6,2),(10,2,14,6),(14,6,10,2),(14,2,10,6),(6,2,10,14),
                                        #      0  * *  3       checks all        *  1  2   *
                                        #      *  5 6  *  <-- 3 in a row-->     4  5  6   7
                                        #      *  9 10 *      above(code)       8  9  10  11
                                        #      12 * *  15                       *  13 14  *
                        (0,1,2,3),(0,2,1,3),(0,3,1,2),(1,2,0,3),(1,3,0,2),(2,3,0,1),
                        (0,4,8,12),(0,8,4,12),(0,12,4,8),(4,8,0,12),(4,12,0,8),(12,8,4,0),
                        (12,13,14,15),(12,14,13,15),(12,15,13,14),(13,14,12,15),(13,15,12,14),(15,14,12,13),
                        (3,7,11,15),(3,11,7,15),(3,15,7,11),(7,11,3,15),(7,15,3,11),(15,11,3,7)]
                                        #      0  1  2  3        check all
                                        #      4  *  *  7   <--  3 in a row
                                        #      8  *  *  11       above(code)
                                        #      12 13 14 15

        for st in squareTuples:
            if( len(_board.board[st[0]])> 0 and _board.board[st[0]][-1] in Y_PIECES and len(_board.board[st[1]])> 0 and _board.board[st[1]][-1] in Y_PIECES ):
                if( len(_board.board[st[2]])> 0 and _board.board[st[2]][-1] in Y_PIECES or len(_board.board[st[3]])> 0 and _board.board[st[3]][-1] in Y_PIECES ):
                    currentvalue +=5

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # The first If statment will check 2 specific index's to see if you have your piece in them, which is part of a possible 3-in-a-row (row/column/diagonal)
        # The second If statment will check if you have any pieces in the same row/column/diagonal of the 2 index's checked in the first If statement
        # which will let us there is a 3-in-a-row then add 5 to you currentvalue


            if( len(_board.board[st[0]])> 0 and _board.board[st[0]][-1] in X_PIECES and len(_board.board[st[1]])> 0 and _board.board[st[1]][-1] in X_PIECES ):
                if( len(_board.board[st[2]])> 0 and _board.board[st[2]][-1] in X_PIECES or len(_board.board[st[3]])> 0 and _board.board[st[3]][-1] in X_PIECES ):
                    currentvalue -=5
        # same as above If statements but checks for other player and subtract 5 form currentvalue

        return currentvalue

    def atTerminalState(self, _board, _depth):
        """
        Checks to see if we've reached a terminal state. Terminal states are:
           * somebody won
           * we have a draw
           * we've hit the depth limit on our search
        Returns a tuple (<terminal>, <value>) where:
           * <terminal> is True if we're at a terminal state, False if we're not
           * <value> is the value of the terminal state
        """
        global DEPTHLIMIT
        # Yay, we won!
        if _board.isWinner(self.myPieces):
            # Return a positive number
            return (True, BIG_POSITIVE_NUMBER)
        # Darn, we lost!
        elif _board.isWinner(_board.opponentPieces(self.name)):
            # Return a negative number
            return (True, BIG_NEGATIVE_NUMBER)
        # if we've hit our depth limit
        elif (_depth >= DEPTHLIMIT):
            # use the evaluation function to return a value for this state
            return (True, self.evaluationFunction(_board))
        return (False, 0)

    def alphaBetaMax(self, _board, _depth = 0, _alpha = NEGATIVE_INFINITY, _beta = POSITIVE_INFINITY):
        '''
        This is the MAX half of alpha-beta pruning. Here is the algorithm:

        int alphaBetaMax( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return evaluate();
           for ( all moves) {
              score = alphaBetaMin( alpha, beta, depthleft - 1 );
              if( score >= beta )
                 return beta;   // fail hard beta-cutoff
              if( score > alpha )
                 alpha = score; // alpha acts like max in MiniMax
           }
           return alpha;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my legal moves
        possibleMoves = _board.possibleNextMoves(self.myPieces)
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # loop through all possible moves
        for m in possibleMoves:
            if (_depth == 0):
                print 'considering ' + str(m) + '...'
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move - move is a tuple: (piece, square)
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMin(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            # compare score to beta - can we prune?
            if (score >= _beta):
                return (mv, _beta)
            # compare score to alpha - have we found a better move?
            if (score > _alpha):
                # keep the better move
                bestMove = m
                # update alpha
                _alpha = score
        # return the best move we found
        return (bestMove, _alpha)

    def alphaBetaMin(self, _board, _depth, _alpha, _beta):
        '''
        This is the MIN half of alpha-beta pruning. Here is the general algorithm:

        int alphaBetaMin( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return -evaluate();
           for ( all moves) {
              score = alphaBetaMax( alpha, beta, depthleft - 1 );
              if( score <= alpha )
                 return alpha; // fail hard alpha-cutoff
              if( score < beta )
                 beta = score; // beta acts like min in MiniMax
           }
           return beta;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my opponent's legal moves
        possibleMoves = _board.possibleNextMoves(_board.opponentPieces(self.name))
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # consider all possible moves
        for m in possibleMoves:
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMax(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            # compare score to alpha - can we prune?
            if (score <= _alpha):
                return (m, _alpha)
            # compare score to the best move we found so far
            if (score < _beta):
                _beta = score
        # send back the best move we found
        return (bestMove, _beta)

    def move(self, _board):


        m = self.alphaBetaMax(_board)[0]
        print "move = " + str(m)


        return m


