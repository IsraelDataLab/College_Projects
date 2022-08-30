#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:30:21 2019

@author: szczurpi
01/18/2019
Spring 1, 2019
Artificial Intelligence
Machine Problem 2 Solution
Gen-Tic-Tac-Toe Minimax Search with alpha/beta pruning
Uses a custom evaluation function for estimating utilities past a maximum depth
"""

import numpy as np
import random
import math

class GenGameBoard: 
    """
    Class responsible for representing the game board and game playing methods
    """
    num_pruned = 0 # counts number of pruned branches due to alpha/beta
    num1 = 0       # counts number of pruned branches due to reaching maximum utility
    numm1 = 0      # counts number of pruned braches due to reaching minimum utility
    MAX_DEPTH = 6  # max depth before applying evaluation function
    depth = 0      # current depth within minimax search
    
    def __init__(self, boardSize):
        """
        Constructor method - initializes each position variable and the board size
        """
        self.boardSize = boardSize  # Holds the size of the board
        self.marks = np.empty((boardSize, boardSize),dtype='str')  # Holds the mark for each position
        self.marks[:,:] = ' '
    
    def printBoard(self): 
        """
        Prints the game board using current marks
        """ 
        # Prthe column numbers
        print(' ',end='')
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
    
    def makeMove(self, row, col, mark):
        """
        Attempts to make a move given the row,col and mark
        If move cannot be made, returns False and prints a message if mark is 'X'
        Otherwise, returns True
        """
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
            print("\nThis position is already taken!")
        
        return possible
    
    def checkWin(self, mark):
        """
        Determines whether a game winning condition exists
        If so, returns True, and False otherwise
        """
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
    
    def noMoreMoves(self):
        """
        Determines whether the board is full
        If full, returns True, and False otherwise
        """
        return (self.marks!=' ').all()

    # TODO - self method should run minimax to determine the value of each move
    # Then make best move for the computer by placing the mark in the best spot
    def makeCompMove(self):
        """
        # This code chooses a random computer move
        # Make sure the move was possible, if not try again
        row, col = -1, -1
        while not self.makeMove(row, col, 'O'):
            col = random.randint(1,boardSize)
            row = random.randint(1,boardSize)
        print("Computer chose: "+str(row)+","+str(col))
        """
        # Make AI move
        bestAction = self.alpha_beta_search()
        self.makeMove(bestAction[0]+1, bestAction[1]+1, 'O')
    
    def is_terminal(self):
        """
        Determines if the current board state is a terminal state
        """
        if self.noMoreMoves() or self.checkWin('X') or self.checkWin('O'):
            return True
        else:
            return False
    
    def get_est_utility(self):
        """
        Implements an evaluation function to estimate the utility of current state
        """
        assert not self.is_terminal()
        points = 0
        
        # Check each row
        for i in range(self.boardSize):
            num_o_in_row = 0
            num_x_in_row = 0
            for j in range(self.boardSize):
                if self.marks[i][j]=='O':
                    num_o_in_row = num_o_in_row + 1
                elif self.marks[i][j]=='X':
                    num_x_in_row = num_x_in_row + 1
            points = points + 10**num_o_in_row - 10**num_x_in_row
            
        # Check each column
        for i in range(self.boardSize):
            num_o_in_row = 0
            num_x_in_row = 0
            for j in range(self.boardSize):
                if self.marks[j][i]=='O':
                    num_o_in_row = num_o_in_row + 1
                elif self.marks[j][i]=='X':
                    num_x_in_row = num_x_in_row + 1
            points = points + 10**num_o_in_row - 10**num_x_in_row

        # Check main diagonal
        num_o_in_row = 0
        num_x_in_row = 0
        for i in range(self.boardSize):
            if self.marks[i][i]=='O':
                num_o_in_row = num_o_in_row + 1
            elif self.marks[i][i]=='X':
                num_x_in_row = num_x_in_row + 1
        points = points + 10**num_o_in_row - 10**num_x_in_row
        
        # Check other diagonal
        num_o_in_row = 0
        num_x_in_row = 0
        for i in range(self.boardSize):
            if self.marks[self.boardSize-1-i][i]=='O':
                num_o_in_row = num_o_in_row + 1
            elif self.marks[self.boardSize-1-i][i]=='X':
                num_x_in_row = num_x_in_row + 1
        points = points + 10**num_o_in_row - 10**num_x_in_row
        
        return points

    def get_utility(self):
        """
        Finds the utility of a terminal state
        """
        assert self.is_terminal()
        if self.checkWin('X'):
            return -10**self.boardSize
        elif self.checkWin('O'):
            return 10**self.boardSize
        else:
            return 0
    
    def get_actions(self):
        '''Generates a list of possible moves'''
        return np.argwhere(self.marks==' ')
    
    def alpha_beta_search(self):
        """
        Go through all possible successor states and generate the max_value
        return action (row,col) that gives the max
        uses the backtracking method
        """
        GenGameBoard.depth = 0
        v,bestAction = self.max_value(-math.inf, math.inf)
        #print('Depth:',GenGameBoard.depth)
        return bestAction
    
    def max_value(self, alpha, beta):
        """
        Finds the action that gives highest minimax value for computer
        Returns both best action and the resulting value
        """
        #print('Depth:',GenGameBoard.depth)
        if self.is_terminal():
            return self.get_utility(), np.array([-1,-1])
        if GenGameBoard.depth > GenGameBoard.MAX_DEPTH:
            return self.get_est_utility(), np.array([-1,-1])
        v = -math.inf
        for action in self.get_actions():
            GenGameBoard.depth = GenGameBoard.depth + 1
            #current_marks = np.array(self.marks) # save current state, so it can be backtracked
            #self.makeMove(action[0]+1, action[1]+1, 'O')
            self.marks[action[0]][action[1]] = 'O'
            minVal = self.min_value(alpha, beta)
            GenGameBoard.depth = GenGameBoard.depth - 1
            if (minVal > v):
                v = minVal
                bestAction = action
            #v = max(v, self.min_value(alpha, beta))
            #self.marks = current_marks # backtrack to prior state
            self.marks[action[0]][action[1]] = ' '

            if v >= 10**self.boardSize:
                GenGameBoard.num1 = GenGameBoard.num1 + 1
                return v, bestAction
            if v >= beta:
                GenGameBoard.num_pruned = GenGameBoard.num_pruned + 1
                return v, bestAction
            alpha = max(alpha, v)
        return v, bestAction
    
    def min_value(self, alpha, beta):
        """
        Finds the action that gives lowest minimax value for computer
        Returns the resulting value
        """
        #print('Depth:',GenGameBoard.depth)
        if self.is_terminal():
            return self.get_utility()
        if GenGameBoard.depth > GenGameBoard.MAX_DEPTH:
            return self.get_est_utility()
        v = math.inf
        for action in self.get_actions():
            GenGameBoard.depth = GenGameBoard.depth + 1
            #current_marks = np.array(self.marks) # save current state, so it can be backtracked
            #self.makeMove(action[0]+1, action[1]+1, 'X')
            self.marks[action[0]][action[1]] = 'X'
            v = min(v, self.max_value(alpha, beta)[0])
            #self.marks = current_marks # backtrack to prior state
            #self.makeMove(action[0]+1, action[1]+1, ' ')
            self.marks[action[0]][action[1]] = ' '
            GenGameBoard.depth = GenGameBoard.depth - 1
            if v <= -(10**self.boardSize):
                GenGameBoard.numm1 = GenGameBoard.numm1 + 1
                return v
            if v <= alpha:
                GenGameBoard.num_pruned = GenGameBoard.num_pruned + 1
                return v
            beta = min(beta, v)
        return v

###########################            
### Program starts here ###
###########################        

# Print out the header info
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: [put your name here]")

# Define constants
LOST = 0
WON = 1
DRAW = 2   
 
#wrongInput = False
# Get the board size from the user
boardSize = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))
        
# Create the game board of the given size and print it
board = GenGameBoard(boardSize)
board.printBoard()  
        
# Start the game loop
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

