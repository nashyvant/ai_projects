import random
def init():
    #d = input("Enter row or column size D?")
    #d = int(d)
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
    return d, ship_map

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

# init the 2D map of ship
d, ship_map = init()
create_ship_layout(ship_map)
print("ship layout:")
print(ship_map)
open_dead_end(ship_map)
print("ship layout after opening dead ends:")
print(ship_map)






