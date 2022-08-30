"""
Created on Thu Nov 12 22:45:18 2020

@author: Malav
"""

import numpy as np
np.set_printoptions(precision=4, suppress=True)

# obstacles are represented as 0
ROBOT_WORLD = np.array([[1, 2, 3, 4],
                        [0, 0, 5, 6],
                        [0, 7, 8, 9],
                        [10, 11, 0, 12]])

num_open_spaces = np.count_nonzero(ROBOT_WORLD)

dirs = [[-1,0], [1,0], [0,1], [0,-1]]   # use directions array for conciseness and scalability of code

# Calculates the transition model and the actual bit vectors at each location.
def calc_transition_model(): 
    transition_model = np.zeros((num_open_spaces, num_open_spaces))
    sensor_bit_vectors = []
    for row in range(ROBOT_WORLD.shape[0]):
        for col in range(ROBOT_WORLD.shape[1]):
            if ROBOT_WORLD[row][col] > 0:
                num_poss_moves = 0
                transition_model_coords = []
                bit_vec = []
                
                for d in dirs:
                    r = row + d[0]
                    c = col + d[1]
                    if r >= 0 and r < ROBOT_WORLD.shape[0] and c >= 0 and c < ROBOT_WORLD.shape[1]:
                        if ROBOT_WORLD[r][c] > 0:
                            num_poss_moves += 1
                            transition_model_coords.append([ROBOT_WORLD[row][col] - 1, ROBOT_WORLD[r][c] - 1])
                            bit_vec.append(0)
                        else:
                            bit_vec.append(1)
                            
                    if r < 0 or r >= ROBOT_WORLD.shape[0] or c < 0 or c >= ROBOT_WORLD.shape[1]:
                        bit_vec.append(1)
                    
                for coord in transition_model_coords:
                    transition_model[coord[0]][coord[1]] = 1 / num_poss_moves

                sensor_bit_vectors.append(bit_vec)
    print(f'Transition Model:\n{transition_model}\n')            
    return transition_model, sensor_bit_vectors

# Calculates emission matrix and final probability. It also shows the tentative location
# of the robot at each time step based on the probabilities.
def calc_observation_model(transition_model, sensor_bit_vectors, observation_mat, eps=0.2):
    prior_prob = np.array([1/num_open_spaces]*num_open_spaces).transpose()
    emission_mat = np.zeros([num_open_spaces, num_open_spaces])
    final_prob_normed = 0
    
    # detect differences in sensor readings vs actual readings
    for observation in observation_mat:
        for n in range(len(sensor_bit_vectors)):
            num_diff = 0
            for m in range(len(sensor_bit_vectors[0])):
                if sensor_bit_vectors[n][m] != observation[m]:
                    num_diff += 1
                    
            emission_mat[n][n] = ((1 - eps)**(4-num_diff)) * (eps**num_diff)
                    
        # apply the HMM      
        final_prob = np.linalg.multi_dot((emission_mat, transition_model.transpose(), prior_prob)) 
        final_prob_normed = final_prob * (1/np.sum(final_prob))
        print(f'\nEmission Matrix:\n{emission_mat}')
        print(f'\nFinal Prob:\n{final_prob_normed}')
        prior_prob = final_prob_normed 
        print(f'\nLikely Location: {np.where(final_prob_normed == np.amax(final_prob_normed))[0] + 1}')

# calculate transition model and get sensor bit vectors
transition_mod, sensor_bit_vecs = calc_transition_model()

# test different epsilon values
print('\nEpsilon: 0.01')
calc_observation_model(transition_mod, sensor_bit_vecs, [[1,1,0,1], [0,1,1,0], [1,0,0,1], [0,1,0,0], [0,0,1,0], [0,0,1,0]], 0.01)  
print('----------------------------------------------------------------------------')   

print('\nEpsilon: 0.2')
calc_observation_model(transition_mod, sensor_bit_vecs, [[1,1,0,1], [0,1,1,0], [1,0,0,1], [0,1,0,0], [0,0,1,0], [0,0,1,0]], 0.2)  
print('----------------------------------------------------------------------------')   

print('\nEpsilon: 0.4')
calc_observation_model(transition_mod, sensor_bit_vecs, [[1,1,0,1], [0,1,1,0], [1,0,0,1], [0,1,0,0], [0,0,1,0], [0,0,1,0]], 0.4)  
print('----------------------------------------------------------------------------')   