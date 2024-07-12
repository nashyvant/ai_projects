import random
import math
import copy
import sys
#from utility import neighbor_weight
from utility import sample_bit

####################################################################
######## creates DxD matrix with user's input ######################
####################################################################
def init(d):
    #d = input("Enter row or column size D?")
    #d = int(d)
    #q = input("Enter q between 0 and 1, defining flammability of the ship?")
    #q = float(q)
    # Check if the correct number of command-line arguments is provided
    
    row, col = (d, d)
    ship_map = [[0 for i in range(col)] for j in range(row)]
    # open a cell at random
    random_row = random.randint(0, d-1)
    random_col = random.randint(0, d-1)
    ship_map[random_row][random_col] = 1
    #print(ship_map)
    return ship_map

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

####################################################################
######## creates the initial ship layout ###########################
####################################################################

def create_ship_layout(ship_map):
    row = len(ship_map)
    col = len(ship_map[0])
    total = 0
    exactly_one_open_neigbor = []
    
    while( 1 ):
        for i in range(row):
            for j in range(col):
                if(ship_map[i][j] == 0):
                    if(i>0):
                        total += ship_map[i-1][j] 
                    if(j < col-1):
                        total += ship_map[i][j+1]
                    if(j > 0):
                        total += ship_map[i][j-1] 
                    if(i < row-1):
                        total += ship_map[i+1][j]
                    if(total == 1):
                        exactly_one_open_neigbor.append((i, j))
                    total = 0
                else:
                    continue
                
        if(len(exactly_one_open_neigbor) == 0):
            return #we are all done
        rand_block_cell = random.randint(0, len(exactly_one_open_neigbor)-1)
        (rand_row, rand_col) = exactly_one_open_neigbor[rand_block_cell]
        ship_map[rand_row][rand_col] = 1
        exactly_one_open_neigbor = []
    return

####################################################################
######## open dead ends - open cells with one open neighbor ########
####################################################################

def open_dead_end(ship_map):
    row = len(ship_map)
    col = len(ship_map[0])
    total = 0
    closed_neighbor_map = {} 
    for i in range(row):
        for j in range(col):
            if(ship_map[i][j] == 1):
                neighbor_list = []
                if(i>0):
                    total += ship_map[i-1][j]
                    if ship_map[i-1][j] == 0:
                        neighbor_list.append((i-1, j))
                if(j < col-1):
                    total += ship_map[i][j+1]
                    if ship_map[i][j+1] == 0:
                        neighbor_list.append((i, j+1))
                if(j > 0):
                    total += ship_map[i][j-1]
                    if ship_map[i][j-1] == 0:
                        neighbor_list.append((i, j-1))
                if(i < row-1):
                    total += ship_map[i+1][j]
                    if ship_map[i+1][j] == 0:
                        neighbor_list.append((i+1, j))
                if(total == 1):
                    if(len(neighbor_list) > 0):
                        closed_neighbor_map[(i,j)] = neighbor_list
                total = 0
                   
    if(len(closed_neighbor_map) == 0):
        return #we are all done
    num_dead_ends = len(closed_neighbor_map)
    num_open_dead_end = num_dead_ends/2
    count = 0
    for curr_neighbors in closed_neighbor_map :
        r_open_cell = random.randint(0, len(closed_neighbor_map[curr_neighbors])-1)
        row, col= closed_neighbor_map[curr_neighbors][r_open_cell]
        #row = row_col[0]
        #col = row_col[1]
        ship_map[row][col] = 1
        count +=1
        if(count >= num_open_dead_end):
            break
    return

####################################################################
######## open unique cells for fire, bot and button  ###############
####################################################################

def create_bot_fire_button(ship_map):
    rand_row = random.randint(0, len(ship_map)-1)
    rand_col = random.randint(0, len(ship_map[0])-1)
    
    while(ship_map[rand_row][rand_col] != 1):
        rand_row = random.randint(0, len(ship_map)-1)
        rand_col = random.randint(0, len(ship_map[0])-1)  
    bot_coord = (rand_row, rand_col)
    
    while((ship_map[rand_row][rand_col] == 0) or (bot_coord == (rand_row, rand_col))):
        rand_row = random.randint(0, len(ship_map)-1)
        rand_col = random.randint(0, len(ship_map[0])-1) 
    button_coord = (rand_row, rand_col)
    
    while(ship_map[rand_row][rand_col] == 0 
          or ((rand_row, rand_col) == bot_coord
          or (rand_row, rand_col) == button_coord)):
        rand_row = random.randint(0, len(ship_map)-1)
        rand_col = random.randint(0, len(ship_map[0])-1)
    fire_coord = (rand_row, rand_col)
    return bot_coord, button_coord, fire_coord

def create_fire_matrix(d, fire_coord):
    row = d
    col = d
    fire_matrix = [[0 for i in range(col)] for j in range(row)]
    fire_matrix[fire_coord[0]][fire_coord[1]] = 1
    return fire_matrix

def update_fire_matrix(ship_map, fire_matrix, q):
    row = len(ship_map)
    col = len(ship_map[0])
    new_fire_matrix = copy.deepcopy(fire_matrix)
    #print("update fire matrix INPUT")
    #for i in range(0, len(ship_map)):
        #print(ship_map[i])

    for i in range(row):
        for j in range(col):
            if(ship_map[i][j] == 1):
                K = 0
                if(i>0 and fire_matrix[i-1][j] == 1):
                    K += 1
                if(j < col-1 and fire_matrix[i][j+1] == 1 ):
                    K += 1
                if(j > 0 and fire_matrix[i][j-1] == 1):
                    K += 1
                if(i < row-1 and fire_matrix[i+1][j] == 1):
                    K += 1 
                #print("K: ", K)
                curr_fire_probability = round(1 - math.pow((1 - q), K), 2)
                #print("fire_matrix[", i,"][", j, "] = ", fire_matrix[i][j])
                new_fire_matrix[i][j] = sample_bit(curr_fire_probability)
                if(new_fire_matrix[i][j] == 1): # cell sets on fire
                    ship_map[i][j] = -1
    fire_matrix = new_fire_matrix
    #print("updated ship matrix with fire OUPUT")
    #for i in range(0, len(ship_map)):
        #print(ship_map[i])
    return fire_matrix

def simulate_fire_matrix(ship_map, fire_matrix, q, steps):
    row = len(ship_map)
    col = len(ship_map[0])
    new_fire_matrix = copy.deepcopy(fire_matrix)

    while(steps):
        for i in range(row):
            for j in range(col):
                if(ship_map[i][j] == -1):
                    K = 0
                    if(i>0 and ship_map[i-1][j] == 1):
                        new_fire_matrix[i-1][j] = 1
                    if(j < col-1 and ship_map[i][j+1] == 1 ):
                        new_fire_matrix[i][j+1] = 1
                    if(j > 0 and ship_map[i][j-1] == 1):
                       new_fire_matrix[i][j-1] = 1
                    if(i < row-1 and ship_map[i+1][j] == 1):
                        new_fire_matrix[i+1][j] = 1
        steps -= 1

    #print("simulated fire matrix")
    #for i in range(0, len(new_fire_matrix)):
        #print(new_fire_matrix[i])

    return new_fire_matrix