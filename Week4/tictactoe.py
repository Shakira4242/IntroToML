import copy
import random

class ExperimentGenerator:
    
    def __init__(self):
        self.board = self.generateBoard()
        self.history = [copy.deepcopy(self.board)]

    def setBoard(self,board):
        if board == 0:
            print "zero board"
        self.board = board
        self.history.append(copy.deepcopy(self.board))

    def generateBoard(self):
        board = [ [0,0,0],
                  [0,0,0],
                  [0,0,0] ]
        return board

    def getWinner(self, board = 0):
        if board == 0:
            board = self.board

        if self.isDone(board):
            
            possibilities = []
            for row in self.getRows(board):
                possibilities.append(row)
            for column in self.getColumns(board):
                possibilities.append(column)
            for diagonal in self.getDiagonals(board):
                possibilities.append(diagonal)
            
            for possibility in possibilities:
                zeros = 0
                Xs = 0
                Os = 0
                for entry in possibility:
                    if entry == 0:
                        zeros += 1
                    elif entry == 1:
                        Xs += 1
                    elif entry == 2:
                        Os += 1
            
                if Xs == 3:
                    return 1
                elif Os == 3:
                    return 2

            return 0

        else:
            print "Game not done, cannot determine winner"

    def isDone(self, board = 0):
        if board == 0:
            board = self.board

        done = True
        for y in range(0,3):
            for x in range(0,3):
                if board[y][x] == 0:
                    done = False
                            
        possibilities = []
        for row in self.getRows(board):
            possibilities.append(row)
        for column in self.getColumns(board):
            possibilities.append(column)
        for diagonal in self.getDiagonals(board):
            possibilities.append(diagonal)
            
        for possibility in possibilities:
            zeros = 0
            Xs = 0
            Os = 0
            for entry in possibility:
                if entry == 0:
                    zeros += 1
                elif entry == 1:
                    Xs += 1
                elif entry == 2:
                    Os += 1
            
            if Xs == 3 or Os == 3:
                done = True
                
        return done

    def getFeatures(self, board = 0):
        if board == 0:
            board = self.board
        #x1 = number of instances of 2 x's in a row with an open subsequent square
        #x2 = number of instances of 2 o's in a row with an open subsequent square
        #x3 = number of instances of an x in an open row or column
        #x4 = number of instances of an o in an open row or column
        #x5 = number of instances of 3 xs in a row
        #x6 = number of instances of 3 os in a row
        possibilities = []
        for row in self.getRows(board):
            possibilities.append(row)
        for column in self.getColumns(board):
            possibilities.append(column)
        for diagonal in self.getDiagonals(board):
            possibilities.append(diagonal)

        x1 = 0      
        x2 = 0
        x3 = 0
        x4 = 0
        x5 = 0
        x6 = 0
        for possibility in possibilities:
            zeros = 0
            Xs = 0
            Os = 0
            for entry in possibility:
                if entry == 0:
                    zeros += 1
                elif entry == 1:
                    Xs += 1
                elif entry == 2:
                    Os += 1
            if Xs == 2 and zeros == 1:
                x1 += 1
            elif Os == 2 and zeros == 1:
                x2 += 1
            elif Xs == 1 and zeros == 2:
                x3 += 1
            elif Os == 1 and zeros == 2:
                x4 += 1
            elif Xs == 3:
                x5 += 1
            elif Os == 3:
                x6 += 1

        return x1,x2,x3,x4,x5,x6

    def getRows(self, board = 0):
        if board == 0:
            board = self.board
        return board
    
    def getColumns(self,board = 0):
        if board == 0:
            board = self.board

        columns = []
        for x in range(0,3):
            column = []
            column.append(board[0][x])
            column.append(board[1][x])
            column.append(board[2][x])
            columns.append(column)

        return columns

    def getDiagonals(self,board = 0):
        if board == 0:
            board = self.board

        diagonals = []

        diagonal1 = []
        diagonal1.append(board[2][0])
        diagonal1.append(board[1][1])
        diagonal1.append(board[0][2])
        diagonals.append(diagonal1)

        diagonal2 = []
        diagonal2.append(board[0][0])
        diagonal2.append(board[1][1])
        diagonal2.append(board[2][2])
        diagonals.append(diagonal2)

        return diagonals

    def getSuccessorsX(self):
        successors = []
        for y in range(0,3):
            for x in range(0,3):
                if self.board[y][x] == 0:
                    successor = copy.deepcopy(self.board)
                    successor[y][x] = 1
                    successors.append(successor)
        return successors

    def getSuccessorsO(self):
        successors = []
        for y in range(0,3):
            for x in range(0,3):
                if self.board[y][x] == 0:
                    successor = copy.deepcopy(self.board)
                    successor[y][x] = 2
                    successors.append(successor)
        return successors

    def getHistory(self):
        return self.history

    def setX(self,x,y):
        self.board[y][x] = 1
        self.history.append(copy.deepcopy(self.board))

    def setO(self,x,y):
        self.board[y][x] = 2

    def printBoard(self, board = 0):
        if board == 0:
            board = self.board

        sboard = []
        for row in board:
            srow = []
            for entry in row:
                if entry == 0:
                    srow.append(' ')
                elif entry == 1:
                    srow.append('X')
                elif entry == 2:
                    srow.append('O')
            sboard.append(srow)

        print ""
        print sboard[0][0] + '|' + sboard[0][1] + '|' + sboard[0][2]
        print "-----"
        print sboard[1][0] + '|' + sboard[1][1] + '|' + sboard[1][2]
        print "-----"
        print sboard[2][0] + '|' + sboard[2][1] + '|' + sboard[2][2]
        print ""


class PerformanceSystem:
    def __init__(self,board,hypothesis,mode = 1):
        self.board = board
        self.hypothesis = hypothesis
        self.mode = mode
        self.history = []        
        self.updateConstant = .1

    def setUpdateConstant(self, constant):
        self.updateConstant = constant

    def evaluateBoard(self,board):
        x1,x2,x3,x4,x5,x6 = self.board.getFeatures(board)

        w0,w1,w2,w3,w4,w5,w6 = self.hypothesis

        return w0 + w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + w6*x6

    def setBoard(self, board):
        self.board = board

    def getBoard(self):
        return self.board

    def setHypothesis(self, hypothesis):
        self.hypothesis = hypothesis

    def getHypothesis(self):
        return self.hypothesis

    def chooseRandom(self):
        if self.mode == 1:
            successors = self.board.getSuccessorsX()
        else:
            successors = self.board.getSuccessorsO()
            
        randomBoard = successors[random.randint(0,len(successors)-1)]
        self.board.setBoard(randomBoard)

    def chooseMove(self):
        if self.mode == 1:
            successors = self.board.getSuccessorsX()
        else:
            successors = self.board.getSuccessorsO()

        bestSuccessor = successors[0]
        bestValue = self.evaluateBoard(bestSuccessor)

        for successor in successors:
            value = self.evaluateBoard(successor)
            if value > bestValue:
                bestValue = value
                bestSuccessor = successor

        self.board.setBoard(bestSuccessor)


    def updateWeights(self,history,trainingExamples):
        for i in range(0,len(history)):
            w0,w1,w2,w3,w4,w5,w6 = self.hypothesis
            vEst = self.evaluateBoard(history[i])
            x1,x2,x3,x4,x5,x6 = trainingExamples[i][0]
            vTrain = trainingExamples[i][1]            

            w0 = w0 + self.updateConstant*(vTrain - vEst)
            w1 = w1 + self.updateConstant*(vTrain - vEst)*x1
            w2 = w2 + self.updateConstant*(vTrain - vEst)*x2
            w3 = w3 + self.updateConstant*(vTrain - vEst)*x3
            w4 = w4 + self.updateConstant*(vTrain - vEst)*x4
            w5 = w5 + self.updateConstant*(vTrain - vEst)*x5
            w6 = w6 + self.updateConstant*(vTrain - vEst)*x6

            self.hypothesis = w0,w1,w2,w3,w4,w5,w6


class Critic:
    def __init__(self,hypothesis,mode = 1):
        self.hypothesis = hypothesis
        self.mode = mode
        self.checker = ExperimentGenerator()
        
    def evaluateBoard(self,board):
        x1,x2,x3,x4,x5,x6 = self.checker.getFeatures(board)

        w0,w1,w2,w3,w4,w5,w6 = self.hypothesis

        return w0 + w1*x1 + w2*x2 + w3*x3 + w4*x4 + w5*x5 + w6*x6

    def setHypothesis(self,hypothesis):
        self.hypothesis = hypothesis

    def setMode(self,mode):
        self.mode = mode

    def getTrainingExamples(self,history):
        trainingExamples = []

        for i in range(0,len(history)):
            if(self.checker.isDone(history[i])):
                if(self.checker.getWinner(history[i]) == self.mode):
                    trainingExamples.append([self.checker.getFeatures(history[i]), 100])
                elif(self.checker.getWinner(history[i]) == 0):
                    trainingExamples.append([self.checker.getFeatures(history[i]), 0])
                else:
                    trainingExamples.append([self.checker.getFeatures(history[i]), -100])
            else:
                if i+2 >= len(history):
                    if(self.checker.getWinner(history[len(history)-1]) == 0):
                        trainingExamples.append([self.checker.getFeatures(history[i]), 0])
                    else:
                        trainingExamples.append([self.checker.getFeatures(history[i]), -100])
                else:
                    trainingExamples.append([self.checker.getFeatures(history[i]), self.evaluateBoard(history[i+2])])

        return trainingExamples

board = ExperimentGenerator()
hypothesis1 = (.5,.5,.5,.5,.5,.5,.5)
hypothesis2 = (.5,.5,.5,.5,.5,.5,.5)
player1 = PerformanceSystem(board,hypothesis1,1)
player2 = PerformanceSystem(board,hypothesis2,2)
player2.setUpdateConstant(.4)
critic1 = Critic(hypothesis1,1)
critic2 = Critic(hypothesis2,2)

xwins = 0
owins = 0
draws = 0

