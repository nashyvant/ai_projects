# importing "heapq" to implement heap queue
import heapq

from create_ship_layout import init, create_ship_layout, open_dead_end, create_bot_fire_button
from create_ship_layout import create_dist_matrix, create_fire_matrix, update_fire_matrix
from utility import weight

#project 1 - bot turns off fire
# init the 2D map of ship
d, ship_map, q = init()
create_ship_layout(ship_map)
print("ship layout:")
print(ship_map)
open_dead_end(ship_map)
print("ship layout after opening dead ends:")
print(ship_map)
bot_coord, button_coord, fire_coord = create_bot_fire_button(ship_map)
#ship_map[fire_coord[0]][fire_coord[1]] = -1

dist_matrix = create_dist_matrix(ship_map, bot_coord, button_coord, fire_coord)
print(dist_matrix)

rows = len(ship_map)
cols = len(ship_map[0])
    
def run_bot1(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    myheap = [(0, bot_coord)]
    while len(myheap) > 0:
        print("fire matrix")
        print(fire_matrix)
        curr_cell = heapq.heappop(myheap)
        print("popping from PQ:", curr_cell)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] != 0):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            return "true"
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        
        if(i>0):
            if(ship_map[i-1][j] == 1 ):
                heapq.heappush(myheap, (dist_matrix[i-1][j], (i-1, j)))
        if(j < cols-1):
            if ship_map[i][j+1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j+1], (i, j+1)))
        if(j > 0):
            if ship_map[i][j-1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j-1], (i, j-1)))
        if(i < rows-1):
            if ship_map[i+1][j] == 1:
                heapq.heappush(myheap, (dist_matrix[i+1][j], (i+1, j)))
        update_fire_matrix(ship_map, fire_matrix, q)
    return "false"

def run_bot2(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    myheap = [(0, bot_coord)]
    while len(myheap) > 0:
        print("fire matrix")
        print(fire_matrix)
        curr_cell = heapq.heappop(myheap)
        print("popping from PQ:", curr_cell)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] != 0):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            return "true"
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        
        print("d is: ", d)
        if(i>0):
            if(ship_map[i-1][j] == 1 ):
                heapq.heappush(myheap, (dist_matrix[i-1][j]+weight(d)*fire_matrix[i-1][j], (i-1, j)))
        if(j < cols-1):
            if ship_map[i][j+1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j+1]+weight(d)*fire_matrix[i][j+1], (i, j+1)))
        if(j > 0):
            if ship_map[i][j-1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j-1]+weight(d)*fire_matrix[i][j-1], (i, j-1)))
        if(i < rows-1):
            if ship_map[i+1][j] == 1:
                heapq.heappush(myheap, (dist_matrix[i+1][j]+weight(d)*fire_matrix[i+1][j], (i+1, j)))
        update_fire_matrix(ship_map, fire_matrix, q)
    return "false"

mission_success = run_bot1(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols)
print("bot1 mission:", mission_success)

print("-----------------------------------------------------------------------------------------------")
mission_success = run_bot2(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols)
print("bot2 mission:", mission_success)
