# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:24:06 2019

@author: Piotr Szczurek

This program implements A* for solving a sliding tile puzzle
"""
import numpy as np
import queue

class PuzzleState():
    SOLVED_PUZZLE = np.arange(9).reshape((3, 3))
    
    def __init__(self,conf,g,predState):
        self.puzzle = conf     # Configuration of the state
        self.gcost = g         # Path cost
        self._compute_heuristic_cost()  # Set heuristic cost
        self.fcost = self.gcost + self.hcost
        self.pred = predState  # Predecesor state
        self.zeroloc = np.argwhere(self.puzzle == 0)[0]
        self.action_from_pred = None
        
    def __hash__(self):
            return tuple(self.puzzle.ravel()).__hash__()
    
    
    
    def _compute_heuristic_cost(self):
        """ Updates the heuristic function value for use in A* """
        self.hcost = 0
        goal_state_0x = 0
        goal_state_1x = 1
        goal_state_2x = 2
        goal_state_0y = 0
        goal_state_1y = 1
        goal_state_2y = 2
        
        loc_of_current_0 = np.argwhere(a == 0)[0] #getting axis value from our 'zero'
        loc_of_current_1 = np.argwhere(a == 1)[0] #number in the array
        loc_of_current_2 = np.argwhere(a == 2)[0]
        loc_of_current_3 = np.argwhere(a == 3)[0]
        loc_of_current_4 = np.argwhere(a == 4)[0]
        loc_of_current_5 = np.argwhere(a == 5)[0]
        loc_of_current_6 = np.argwhere(a == 6)[0]
        loc_of_current_7 = np.argwhere(a == 7)[0]
        loc_of_current_8 = np.argwhere(a == 8)[0]
        
        #Unfortunatelly, I am not great with for loops, thus manual calculation
        
        manhattan_distance0 = abs(loc_of_current_0[0] - goal_state_0x) \
            + abs(loc_of_current_0[1] - goal_state_0y)

        manhattan_distance1 = abs(loc_of_current_1[0] - goal_state_0x) + \
            abs(loc_of_current_1[1] - goal_state_1y)

        manhattan_distance2 = abs(loc_of_current_2[0] - goal_state_0x) + \
            abs(loc_of_current_2[1] - goal_state_2y)
        
        manhattan_distance3 = abs(loc_of_current_3[0] - goal_state_1x) + \
            abs(loc_of_current_3[1] - goal_state_0y)
        
        manhattan_distance4 = abs(loc_of_current_4[0] - goal_state_1x) + \
            abs(loc_of_current_4[1] - goal_state_1y)
        
        manhattan_distance5 = abs(loc_of_current_5[0] - goal_state_1x) + \
            abs(loc_of_current_5[1] - goal_state_2y)
        
        manhattan_distance6 = abs(loc_of_current_6[0] - goal_state_2x) + \
            abs(loc_of_current_6[1] - goal_state_0y)
        
        manhattan_distance7 = abs(loc_of_current_7[0] - goal_state_2x) + \
            abs(loc_of_current_7[1] - goal_state_1y)
     
        manhattan_distance8 = abs(loc_of_current_8[0] - goal_state_2x) + \
            abs(loc_of_current_8[1] - goal_state_2y)
        
        self.hcost = manhattan_distance1 + manhattan_distance2 + manhattan_distance3 + \
            manhattan_distance4 + manhattan_distance5 + manhattan_distance6 + \
                manhattan_distance7 + manhattan_distance8
                
        return self.hcost
    
     
        
    
    def is_goal(self):
     
        return np.array_equal(PuzzleState.SOLVED_PUZZLE,self.puzzle)
        
    def __lt__(self, other):
        return self.fcost < other.fcost
    
    def __str__(self):
        return np.str(self.puzzle)
    
    move = 0
    
    def show_path(self):
        if self.pred is not None:
            self.pred.show_path()
        
        if PuzzleState.move==0:
            print('START')
        else:
            print('Move',PuzzleState.move, 'ACTION:', self.action_from_pred)
        PuzzleState.move = PuzzleState.move + 1
        print(self)
        
  
    
    def can_move(self, direction):
                
        if direction == 'up':
            return self.zeroloc[0] > 0
        
        elif direction == 'down':
            return self.zeroloc[0] < 2
             
        elif direction == 'left':
            return self.zeroloc[1] > 0
            
        elif direction == 'right':
            return self.zeroloc[1] < 2
        
        
    def gen_next_state(self, direction):
      move_state = PuzzleState(self.puzzle,num_states,self)
      
      if direction == 'up':
               print('move up')
               self.puzzle[self.zeroloc[0], self.zeroloc[1]] = self.puzzle[self.zeroloc[0]-1, self.zeroloc[1]]
               self.puzzle[self.zeroloc[0]-1,self.zeroloc[1]] = 0
      
      elif direction == 'down':
            print('move down')
            self.puzzle[self.zeroloc[0],self.zeroloc[1]] = self.puzzle[self.zeroloc[0]+1,self.zeroloc[1]]
            self.puzzle[self.zeroloc[0]+1,self.zeroloc[1]] = 0
        
      elif direction == 'left':
            print('move left')
            self.puzzle[self.zeroloc[0],self.zeroloc[1]] = self.puzzle[self.zeroloc[0],self.zeroloc[1]-1]
            self.puzzle[self.zeroloc[0],self.zeroloc[1]-1] = 0
       
      elif direction == 'right':
            print('move right')
            self.puzzle[self.zeroloc[0],self.zeroloc[1]] = self.puzzle[self.zeroloc[0],self.zeroloc[1]+1]
            self.puzzle[self.zeroloc[0],self.zeroloc[1]+1] = 0
     
      self.zeroloc = np.argwhere(self.puzzle == 0)[0]
      self.pred = move_state
      self._compute_heuristic_cost()
      self.fcost = self.gcost + self.hcost
      self.action_from_pred = direction
      print(self.puzzle)
      return move_state
    
            

print('Artificial Intelligence')
print('MP1: A* for Sliding Puzzle')
print('SEMESTER: Fall I')
print('NAME: Israel Nolazco')
print()

# load random start state onto frontier priority queue
frontier = queue.PriorityQueue()
a = np.loadtxt('mp1input.txt', dtype=np.int32)

start_state = PuzzleState(a,0,None)

frontier.put(start_state)

closed_set = set()

num_states = 0
while not frontier.empty():
    #  choose state at front of priority queue
    next_state = frontier.get()
    num_states = num_states + 1

    #  if goal then quit and return path
    if next_state.is_goal():
        next_state.show_path()
        break
    
    # Add state chosen for expansion to closed_set
    closed_set.add(next_state)
    
    # Expand state (up to 4 moves possible)
    possible_moves = ['up','down','left','right']
    for move in possible_moves:
        if next_state.can_move(move):
            neighbor = next_state.gen_next_state(move)
            if neighbor in closed_set:
                continue
            if neighbor not in frontier.queue:                           
                frontier.put(neighbor)
            # If it's already in the frontier, it's gauranteed to have lower cost, so no need to update

print('\nNumber of states visited =',num_states)


