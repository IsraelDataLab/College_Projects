#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:30:21 2019

@author: szczurpi

Machine Problem 2
Gen-Tic-Tac-Toe Minimax Search with alpha/beta pruning
"""

"""
Israel Nolazco
September 28, 2020
Artificial Intellegence 1
Fall 1
Machine Problem 2
"""

import numpy as np
import random
import math

# self class is responsible for representing the game board
class GenGameBoard: 
    
    # Constructor method - initializes each position variable and the board size
    def __init__(self, boardSize):
        self.boardSize = boardSize  # Holds the size of the board
        self.marks = np.empty((boardSize, boardSize),dtype='str')  # Holds the mark for each position
        self.marks[:,:] = ' '
    
    # Prints the game board using current marks
    def printBoard(self): 
        # Prthe column numbers
        print(' ',end = '')
        for j in range(self.boardSize):
            print(" "+str(j+1), end='')
        
        
        # Prthe rows with marks
        print("")
        for i in range(self.boardSize):
            # Prthe line separating the row
            print(" ",end='')
            for j in range(self.boardSize):
                print("--",end='')
            
            print("-")

            # Prthe row number
            print(i+1,end='')
            
            # Prthe marks on self row
            for j in range(self.boardSize):
                print("|"+self.marks[i][j],end='')
            
            print("|")
                
        
        # Prthe line separating the last row
        print(" ",end='')
        for j in range(self.boardSize):
            print("--",end='')
        
        print("-")
    
    
    # Attempts to make a move given the row,col and mark
    # If move cannot be made, returns False and prints a message if mark is 'X'
    # Otherwise, returns True
    def makeMove(self, row, col, mark):
        possible = False  # Variable to hold the return value
        if row==-1 and col==-1:
            return False
        
        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1
        
        if row<0 or row>=self.boardSize or col<0 or col>=self.boardSize:
            print("Not a valid row or column!")
            return False
        
        # Check row and col, and make sure space is empty
        # If empty, set the position to the mark and change possible to True
        if self.marks[row][col] == ' ':
            self.marks[row][col] = mark
            possible = True    
        
        # Prout the message to the player if the move was not possible
        if not possible and mark=='X':
            print("\nself position is already taken!")
        
        return possible
    
    
    # Determines whether a game winning condition exists
    # If so, returns True, and False otherwise
    def checkWin(self, mark):
        won = False # Variable holding the return value
        
        # Check wins by examining each combination of positions
        
        # Check each row
        for i in range(self.boardSize):
            won = True
            for j in range(self.boardSize):
                if self.marks[i][j]!=mark:
                    won=False
                    break        
            if won:
                break
        
        # Check each column
        if not won:
            for i in range(self.boardSize):
                won = True
                for j in range(self.boardSize):
                    if self.marks[j][i]!=mark:
                        won=False
                        break
                if won:
                    break

        # Check first diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[i][i]!=mark:
                    won=False
                    break
                
        # Check second diagonal
        if not won:
            for i in range(self.boardSize):
                won = True
                if self.marks[self.boardSize-1-i][i]!=mark:
                    won=False
                    break

        return won
    
    # Determines whether the board is full
    # If full, returns True, and False otherwise
    def noMoreMoves(self):
        return (self.marks!=' ').all()
    
    def makeCompMove(self):
        # This code chooses a random computer move - just for testing purposes
        # REMOVE THIS AFTER IMPLEMENTING AI
        # Make sure the move was possible, if not try again
        row, col = self.alphaBetaSearch(self.marks)
        row +=1
        col +=1
        print("Computer chose: "+str(row)+","+str(col))
     
        # Run alpha beta search here
    
    def alphaBetaSearch(self, state):
        v, bestAction = self.maxValue(state, -math.inf, math.inf)
        
        
        return bestAction  

    
    def maxValue(self, state, alpha, beta): 
        #returns a utility value and an action
        #state is a matrix argwhere find all empty locations
        
        if self.terminalTest(state): #could mean check move function
            return self.utility(state)
        
        v = -math.inf
        
        for action in self.actions(state):
            min_v = self.minValue(self.result(state,action), alpha, beta)
            
            if min_v > v:
                v = min_v
                best_action = action 
                
            if v >= beta: 
                return v
            alpha = max(alpha,v)
            
        return v,best_action
    
    def minValue(self,state, alpha, beta): #return a utility value
        if self.terminalTest(state):
            return self.utility(state)
        
        v = math.inf
        
        for action in self.actions(state):
            v = min(v, self.maxValue(self.result(state,action), alpha, beta)[0])
            
            if v <= alpha:
                return v
            
            beta = min(beta,v)
            
        return v    
    
    def terminalTest (self, state):  
        #should this return boolean?
        #Terminal state: check if board is full.  
        #if Min Wins or Max wins is a terminal state
        
        state = np.argwhere((self.marks!=' ').all()) #the board is full
        print(state)
        
        if state:        
            return  True
        
        if not state:
            if self.checkWin('X'):
                return True
            
            elif self.checkWin('O'):
                return True
    
    def actions (self, state):
        #action return possible moves(empty locations) for given state
        #getting an error associated with action
        #could be because I am using an empty array
        
        open_space = 0
        
        for i in range (self.boardSize):
            for j in range (self.boardSize): #looking for empty spaces
                if state [i][j] == ' ': #in the board
                    open_space +=1
        
        if open_space % 2 == 0 :
            open_space +=1                   
        
        if self.checkWin(state,'X'):
            return state
            
        elif self.checkWin(state, 'O'):
            return state        
        
        return state
    
    def result (self, state, action, mark):
        row,col = action
        state = np.copy(state)
        state[row][col] = mark
        return state
    
    def utility(self,state):
    #Utility, if board is full is zero, if max wins, then is 1, if min wins is -1    
    #checks win for a given matrix in the check win or no more moves  
        
        open_space = 0
        
        for i in range (self.boardSize):
            for j in range (self.boardSize):
                if state [i][j] == ' ':
                    open_space +=1
                    
        if open_space % 2 == 0 :
            open_space +=1
            
        utility = None
        if self.checkWin(state,'X'):
            utility = -1
            
        elif self.checkWin(state,'O'):
            utility = 1
        else:
            utility = 0
        
        return utility * open_space
        
  
#    def terminalTest (self, state):    
    
#    def utility(self, state): 
        
#    def actions (self, state):
        
#    def result (self, state, action): 
         
    
"""
psudeo code 
        function ALPHA-BETA-SEARCH(state)returns an action
            v <- MAX-VALUE(state,-inf, +inf)
            return the action in ACTIONS (state) with value v
        
        function MAX-VALUE (state,alpha, beta ) returns a utility value
            if TERMINAL-TEST(STATE) then return Utility(state)
            v <- -inf
            for each a in Actions(state) do
                v <- MAX(V,MIN-VALUE(RESULTS(state,action),alpha,beta))
                if v >= beta then return v
                alpha <- MAX(alpha,v)
                return v
            
        function MIN-VALUE(state,alpha, beta) returns a utility value 
            if TERMINAL-TEST(state) then return Utility(state)
            v <- inf
            for each a in Actions(state) do
            v <- MIN(v,MAX-VALUE(RESULT(satate,action), alpha, beta))
            if v<= alpha then return v
            beta <- MIN(beta,v)
            return v
"""
        
        

# Print out the header info
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Israel Nolazco")

LOST = 0
WON = 1
DRAW = 2    
wrongInput = False
boardSize = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))
        
# Create the game board of the given size
board = GenGameBoard(boardSize)
        
board.printBoard()  # Print the board before starting the game loop
        
# Game loop
while True:
    # *** Player's move ***        
    
    # Try to make the move and check if it was possible
    # If not possible get col,row inputs from player    
    row, col = -1, -1
    while not board.makeMove(row, col, 'X'):
        print("Player's Move")
        row, col = input("Choose your move (row, column): ").split(',')
        row = int(row)
        col = int(col)

    # Display the board again
    board.printBoard()
            
    # Check for ending condition
    # If game is over, check if player won and end the game
    if board.checkWin('X'):
        # Player won
        result = WON
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break
            
    # *** Computer's move ***
    board.makeCompMove()
    
    # Print out the board again
    board.printBoard()    
    
    # Check for ending condition
    # If game is over, check if computer won and end the game
    if board.checkWin('O'):
        # Computer won
        result = LOST
        break
    elif board.noMoreMoves():
        # No moves left -> draw
        result = DRAW
        break
        
# Check the game result and print out the appropriate message
print("GAME OVER")
if result==WON:
    print("You Won!")            
elif result==LOST:
    print("You Lost!")
else: 
    print("It was a draw!")