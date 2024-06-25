import random
import math

####################################################################
######## creates DxD matrix with user's input ######################
####################################################################
def init():
    #d = input("Enter row or column size D?")
    #d = int(d)
    #q = input("Enter q between 0 and 1, defining flammability of the ship?")
    #q = input(q)
    q = 0.5
    d = 5
    row, col = (d, d)
    ship_map = [[0 for i in range(col)] for j in range(row)]
    print(ship_map)
    # open a cell at random
    random_row = random.randint(0, d-1)
    random_col = random.randint(0, d-1)
    print(random_row, random_col)
    ship_map[random_row][random_col] = 1
    print(ship_map)
    return d, ship_map, q

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
    print("bot @ ", bot_coord, " button @ ", button_coord, " fire @ ", fire_coord)
    return bot_coord, button_coord, fire_coord

def create_dist_matrix(ship_map, bot_coord, button_coord, fire_coord):
    row = len(ship_map)
    col = len(ship_map[0])
    dist_matrix = [[0 for i in range(col)] for j in range(row)]
    for i in range(row):
        for j in range(col):
            dist_matrix[i][j] = math.sqrt((button_coord[0]-i)*(button_coord[0]-i)+(button_coord[1]-j)*(button_coord[1]-j))
    return dist_matrix

def create_fire_matrix(ship_map, fire_coord):
    row = len(ship_map)
    col = len(ship_map[0])
    fire_matrix = [[0 for i in range(col)] for j in range(row)]
    fire_matrix[fire_coord[0]][fire_coord[1]] = 1
    return fire_matrix

def update_fire_matrix(ship_map, fire_matrix, q):
    row = len(ship_map)
    col = len(ship_map[0])
    for i in range(row):
        for j in range(col):
            if(ship_map[i][j] == 1 and fire_matrix[i][j] == 0):
                K = 0
                if(i>0 and ship_map[i-1][j] == 1):
                    if(fire_matrix[i-1][j] > 0):
                        K += 1
                if(j < col-1 and ship_map[i][j+1] == 1):
                    if fire_matrix[i][j+1] > 0:
                        K += 1
                if(j > 0 and ship_map[i][j-1] == 1):
                    if fire_matrix[i][j-1] > 0:
                        K += 1
                if(i < row-1 and ship_map[i+1][j] == 1 ):
                    if fire_matrix[i+1][j] > 0:
                        K += 1
                        
                fire_matrix[i][j] = 1-math.pow((1-q), K)

