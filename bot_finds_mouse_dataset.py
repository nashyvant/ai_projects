# importing "heapq" to implement heap queue
import heapq
import sys
import copy
import math
import random
import numpy as np
import torch

# Initialize lists to collect input and output tensors
input_data = []
output_data = []

#from utility import weight
from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# Print the current date and time
print("Current Date and Time:", current_time)

# Define the directions for moving in the matrix
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

d = int(40)
alpha = 0.4

'''
if len(sys.argv) != 2:
    print("Usage: python main.py <float_arg>")

alpha = float(sys.argv[1])
print("Automating for alpha: ", alpha, " d: ", d)
'''

ship_map = [
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1]
]

####################################################################
######## creates DxD matrix with probabilitic knowledge base of ####
######## where the mouse is ########################################
####################################################################
def create_pkb(ship_map):
    row, col = (len(ship_map), len(ship_map[0]))
    num_open_cells = 0
    for i in range(0, len(ship_map)):
        for j in range(0, len(ship_map[i])):
            if(ship_map[i][j] == 1):
                num_open_cells += 1
    print("num of open cells:", num_open_cells)
    uniform_dist = 1/(num_open_cells*num_open_cells)
    pkb = [[uniform_dist for i in range(col)] for j in range(row)]

    for i in range(0, len(pkb)):
        for j in range(0, len(pkb[i])):
            if(ship_map[i][j] == 0):
                pkb[i][j] = 0

    return pkb

def sample_bit(p):
    if random.random() <= p :
        return 1
    else:
        return 0
    
def get_path(parent, curr):
    complete_path = [curr]
    steps = 0
    while curr in parent:
        curr = parent[curr]
        complete_path.append(curr)
        steps += 1
    complete_path.reverse()
    return complete_path, steps

pkb = create_pkb(ship_map)

bot_coord = (9, 34)  
mouse_coord = (16, 17)

rows = len(ship_map)
cols = len(ship_map[0])

def print_bot_map(bot_coord):
    #print("bot is now at:", bot_coord)
    bot_map = [[0 for i in range(d)] for j in range(d)]
    bot_map[bot_coord[0]][bot_coord[1]] = 1
    return bot_map
    for i in range(0, d):
        print(bot_map[i])

def heuristic(a, b):
    return round((abs(a[0] - b[0]) + abs(a[1] - b[1])), 8)

def update_known_pkb(bot_coord): # we are at the current cell and know if the mouse is not here, update PKB
    pkb[bot_coord[0]][bot_coord[1]] = 0
    return

def update_pkb(bot_coord, is_beep):
    sum = 0
    for i in range(0, len(pkb)):
        for j in range(0, len(pkb[i])):
            d = heuristic(bot_coord, (i, j))
            updated_prob = 0
            if(is_beep):
                updated_prob = round(pkb[i][j]*(math.exp(-alpha*(d-1))), 8)
            else:    
                updated_prob = round(pkb[i][j]*(1-math.exp(-alpha*(d-1))), 8)
            if(updated_prob < 0 or updated_prob <= -0):
                pkb[i][j] = 0.0
            else:
                pkb[i][j] = updated_prob
            sum += pkb[i][j]

    for i in range(0, len(pkb)):
        for j in range(0, len(pkb[i])):
            pkb[i][j] = round(pkb[i][j]/sum, 8)
    
    return

def mouse_sensor(bot_coord):
    d = heuristic(bot_coord, mouse_coord)
    beep_prob = math.exp(-alpha*(d-1))
    return sample_bit(beep_prob)

def sense(bot_coord):
    is_beep = mouse_sensor(bot_coord)
    update_pkb(bot_coord, is_beep)
    return is_beep

def get_max_likelihood_neighbor(bot_coord):
    new_bot_coord = []
    max_prob = 0
    for x, y in DIRECTIONS: #first get the max P
        neighbor = (bot_coord[0]+x, bot_coord[1]+y)
        if (0 <= neighbor[0] < d and 0 <= neighbor[1] < d) and (ship_map[neighbor[0]][neighbor[1]] == 1): #ignores fire and block cells
            if(pkb[neighbor[0]][neighbor[1]] > max_prob):
                max_prob = pkb[neighbor[0]][neighbor[1]] #gets the max P across 4 neighbors

    for x, y in DIRECTIONS: #now get all the neighbors with the same max probability
        neighbor = (bot_coord[0]+x, bot_coord[1]+y)  
        if (0 <= neighbor[0] < d and 0 <= neighbor[1] < d) and (ship_map[neighbor[0]][neighbor[1]] == 1): #ignores fire and block cells
            if(pkb[neighbor[0]][neighbor[1]]  == max_prob):
                new_bot_coord.append(neighbor)
                
    #print("number of max likelihood neighbors: ", new_bot_coord)
    r = random.randint(0, len(new_bot_coord)-1)
    #print("picking neighbor:", new_bot_coord[r])
    return new_bot_coord[r]

def get_overall_max_likelihood_coord(bot_coord):
    new_bot_coord = []
    max_prob = pkb[bot_coord[0]][bot_coord[1]]
    for i in range(0, len(pkb)):
        for j in range(0, len(pkb[i])):
            if(pkb[i][j] > max_prob):
                max_prob = pkb[i][j] #gets the max P

    for i in range(0, len(pkb)):
        for j in range(0, len(pkb[i])):
            if(pkb[i][j] == max_prob):
                new_bot_coord.append((i, j))

    #print("number of overall max likelihood cells: ", new_bot_coord)
    r = random.randint(0, len(new_bot_coord)-1)
    #print("picking max P cell:", new_bot_coord[r])
    return new_bot_coord[r]

def a_star(ship_map, start, goal):
    myheap = []
    heapq.heappush(myheap, (0, start))
    parent = {}
    cost = {start : 0}
    est_total_cost = {start : heuristic(start, goal)}
    
    while myheap:
        curr_cell = heapq.heappop(myheap)
        if(curr_cell[1] == goal):
            #print("bot finds path to button! ")
            return get_path(parent, curr_cell[1])
    
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        #print("processing i:", i, "j: ", j)

        for x, y in DIRECTIONS:
            neighbor = (curr_cell[1][0]+x, curr_cell[1][1]+y)
            if (0 <= neighbor[0] < d and 0 <= neighbor[1] < d) and (ship_map[neighbor[0]][neighbor[1]] == 1): #block and zero prob cells
                est_curr_cost = cost[curr_cell[1]]+1

                if neighbor not in cost or est_curr_cost < cost[neighbor]:
                    parent[neighbor] = curr_cell[1]
                    cost[neighbor] = est_curr_cost
                    est_total_cost[neighbor] = est_curr_cost+heuristic(neighbor, goal)
                    heapq.heappush(myheap, (est_total_cost[neighbor], neighbor))
                    #print("neighbor:", neighbor, "est curr and total cost of neighbor is: ", est_curr_cost, est_total_cost[neighbor])

        #print(myheap)
    return None, 0
    
def run_bot(ship_map, bot_coord, mouse_coord, bot_num):
    total_actions = 0
    while(True):
        
        bot_map = print_bot_map(bot_coord)
        
        # Stack the matrices into a 3x40x40 tensor
        input_tensor = np.stack((ship_map, pkb, bot_map), axis = 0)
        # Store the input tensor
        input_data.append(torch.tensor(input_tensor, dtype=torch.float32))
        if(bot_coord == mouse_coord):
            #print("bot found the mouse!")
            return 1, total_actions
        
        update_known_pkb(bot_coord) # we are at the current cell and know if the mouse is not here, update PKB

        output = [0, 0, 0, 0, 1]
        output_data.append(torch.tensor(output))

        is_beep = sense(bot_coord)
        #print("At ", bot_coord, " bot beeped:", is_beep)
        total_actions = total_actions+1 # for sensing
        next_bot_coord = get_overall_max_likelihood_coord(bot_coord)
        if(next_bot_coord == bot_coord): # need new coordinates so looking for neighbors
            #print("new coords same as old bot cords", next_bot_coord, bot_coord)
            next_bot_coord = get_max_likelihood_neighbor(bot_coord)

        path, steps = a_star(ship_map, bot_coord, next_bot_coord)
        if path is None:
            #print("ALERT! Cannot find a_star path from ", bot_coord, " to ", next_bot_coord)
            return 0, 0
        #else:
            #print(f"Path to next highest probability: {path}")
        
        k = 1
        while(k < len(path) and pkb[path[k][0]][path[k][1]] <= 0):
            #print("Skip sensing bot_coord: ", path[k], " its PKB is:", pkb[path[k][0]][path[k][1]])
         
            bot_map = print_bot_map(bot_coord)

            # Stack the matrices into a 3x40x40 tensor
            input_tensor = np.stack((ship_map, pkb, bot_map), axis = 0)
            # Store the input tensor
            input_data.append(torch.tensor(input_tensor, dtype=torch.float32))

            for x, y in DIRECTIONS: #first get the max P
                bot_move = (bot_coord[0]+x, bot_coord[1]+y)
                if (0 <= bot_move[0] < d and 0 <= bot_move[1] < d): #ignores fire and block cells
                    if(path[k] == bot_move):
                        if(x == -1 and y == 0):
                            output = [1, 0, 0, 0, 0]
                        if(x == +1 and y == 0):
                            output = [0, 1, 0, 0, 0]
                        if(x == 0 and y == -1):
                            output = [0, 0, 1, 0, 0]
                        if(x == 0 and y == +1):
                            output = [0, 0, 0, 1, 0]
                        break
            output_data.append(torch.tensor(output))
            bot_coord = path[k]
            k  = k+1
        
        bot_map = print_bot_map(bot_coord)
        # Stack the matrices into a 3x40x40 tensor
        input_tensor = np.stack((ship_map, pkb, bot_map), axis = 0)
        # Store the input tensor
        input_data.append(torch.tensor(input_tensor, dtype=torch.float32))

        for x, y in DIRECTIONS: #first get the max P
            bot_move = (path[k-1][0]+x, path[k-1][1]+y)
            if (0 <= bot_move[0] < d and 0 <= bot_move[1] < d): #ignores fire and block cells
                if(path[k] == bot_move):
                    if(x == -1 and y == 0):
                        output = [1, 0, 0, 0, 0]
                    if(x == +1 and y == 0):
                        output = [0, 1, 0, 0, 0]
                    if(x == 0 and y == -1):
                        output = [0, 0, 1, 0, 0]
                    if(x == 0 and y == +1):
                        output = [0, 0, 0, 1, 0]
                    break
        output_data.append(torch.tensor(output))
        bot_coord = path[k]
        total_actions = total_actions+1+(k-1) # move one step



print("----------------------BOT2---------------------------------------------------------------------")
mission_success_2, total_actions_2 = run_bot(ship_map, bot_coord, mouse_coord, 2)

print("alpha is: ", alpha, " D is:", d)
print("bot @ ", bot_coord, " mouse @ ", mouse_coord)
print("bot2 mission:", mission_success_2, "total # of actions", total_actions_2)

# Convert lists to tensors when done collecting data
input_data = torch.stack(input_data)
output_data = torch.stack(output_data)

print("-----------------------------ALL DONE----------------------------------------------------------")
# Open a file in append mode ('a')
with open('mouse_dataset.txt', 'a') as file:
    file.write(f"alpha: {alpha:0.2f}, d: {d}, bot2_actions: {total_actions_2}\n")
