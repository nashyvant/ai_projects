# importing "heapq" to implement heap queue
import heapq
import sys

from create_ship_layout import init, create_ship_layout, open_dead_end, create_bot_fire_button
from create_ship_layout import create_dist_matrix, create_fire_matrix, update_fire_matrix, get_adj_fire_cell_weight
from utility import weight

'''
d = input("Enter row or column size D?")
d = int(d)
q = input("Enter q between 0 and 1, defining flammability of the ship?")
q = float(q)

'''


#project 1 - bot turns off fire
# init the 2D map of ship
if len(sys.argv) != 3:
        print("Usage: python main.py <integer_arg> <float_arg>")

    # Retrieve command-line arguments
d = int(sys.argv[1])
q = float(sys.argv[2])

ship_map = init(d, q)
create_ship_layout(ship_map)
print("ship layout:")
#for i in range(0, len(ship_map)):
    #print(ship_map[i])
open_dead_end(ship_map)
print("ship layout after opening dead ends:")
for i in range(0, len(ship_map)):
    print(ship_map[i])
bot_coord, button_coord, fire_coord = create_bot_fire_button(ship_map)
ship_map[fire_coord[0]][fire_coord[1]] = -1

dist_matrix = create_dist_matrix(ship_map, bot_coord, button_coord, fire_coord)
for i in range(0, len(dist_matrix)):
    print(dist_matrix[i])

rows = len(ship_map)
cols = len(ship_map[0])
    
def run_bot1(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    myheap = [(0, bot_coord)]
    while len(myheap) > 0:
        curr_cell = heapq.heappop(myheap)
        print("bot1 moves to:", curr_cell)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] != 0):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            return "true"
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)
        print("fire matrix")
        for i in range(0, len(fire_matrix)):
            print(fire_matrix[i])

        if(i>0):
            if ship_map[i-1][j] == 1 : #ignores initial fire cell
                heapq.heappush(myheap, (dist_matrix[i-1][j], (i-1, j)))
        if(j < cols-1):
            if ship_map[i][j+1] == 1 : #ignores initial fire cell
                heapq.heappush(myheap, (dist_matrix[i][j+1], (i, j+1)))
        if(j > 0):
            if ship_map[i][j-1] == 1 : #ignores initial fire cell
                heapq.heappush(myheap, (dist_matrix[i][j-1], (i, j-1)))
        if(i < rows-1):
            if ship_map[i+1][j] == 1 : #ignores initial fire cell
                heapq.heappush(myheap, (dist_matrix[i+1][j], (i+1, j)))
    return "false"

def run_bot2(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    myheap = [(0, bot_coord)]
    while len(myheap) > 0:
        curr_cell = heapq.heappop(myheap)
        print("bot2 moves to:", curr_cell)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] != 0):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            return "true"
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)
        print("fire matrix")
        for i in range(0, len(fire_matrix)):
            print(fire_matrix[i])

        if(i>0):
            if(ship_map[i-1][j] == 1 ):
                heapq.heappush(myheap, (dist_matrix[i-1][j]+(weight(d)*fire_matrix[i-1][j]), (i-1, j)))
        if(j < cols-1):
            if ship_map[i][j+1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j+1]+(weight(d)*fire_matrix[i][j+1]), (i, j+1)))
        if(j > 0):
            if ship_map[i][j-1] == 1:
                heapq.heappush(myheap, (dist_matrix[i][j-1]+(weight(d)*fire_matrix[i][j-1]), (i, j-1)))
        if(i < rows-1):
            if ship_map[i+1][j] == 1:
                heapq.heappush(myheap, (dist_matrix[i+1][j]+(weight(d)*fire_matrix[i+1][j]), (i+1, j)))
    return "false"

def run_bot3(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    myheap = [(0, bot_coord)]
    while len(myheap) > 0:
        curr_cell = heapq.heappop(myheap)
        print("bot3 moves to:", curr_cell)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] != 0):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            return "true"
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        
        print("fire matrix")
        for i in range(0, len(fire_matrix)):
            print(fire_matrix[i])

        if(i>0):
            if(ship_map[i-1][j] == 1 ):
                adj_cell_weight = get_adj_fire_cell_weight(ship_map, fire_matrix, rows, cols, i-1, j)
                heapq.heappush(myheap, (dist_matrix[i-1][j]+(weight(d)*fire_matrix[i-1][j])+adj_cell_weight, (i-1, j)))
        if(j < cols-1):
            if ship_map[i][j+1] == 1:
                adj_cell_weight = get_adj_fire_cell_weight(ship_map, fire_matrix, rows, cols, i, j+1)
                heapq.heappush(myheap, (dist_matrix[i][j+1]+(weight(d)*fire_matrix[i][j+1])+adj_cell_weight, (i, j+1)))
        if(j > 0):
            if ship_map[i][j-1] == 1:
                adj_cell_weight = get_adj_fire_cell_weight(ship_map, fire_matrix, rows, cols, i, j-1)
                heapq.heappush(myheap, (dist_matrix[i][j-1]+(weight(d)*fire_matrix[i][j-1])+adj_cell_weight, (i, j-1)))
        if(i < rows-1):
            if ship_map[i+1][j] == 1:
                adj_cell_weight = get_adj_fire_cell_weight(ship_map, fire_matrix, rows, cols, i+1, j)
                heapq.heappush(myheap, (dist_matrix[i+1][j]+(weight(d)*fire_matrix[i+1][j])+adj_cell_weight, (i+1, j)))
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)
    return "false"

print("-----------------------------------------------------------------------------------------------")
mission_success_1 = run_bot1(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols)
print("-----------------------------------------------------------------------------------------------")
mission_success_2 = run_bot2(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols)
print("-----------------------------------------------------------------------------------------------")
mission_success_3 = run_bot3(ship_map, bot_coord, button_coord, fire_coord, dist_matrix, rows, cols)
print("-----------------------------------------------------------------------------------------------")
print("Q is: ", q, " D is:", d)
print("bot @ ", bot_coord, " button @ ", button_coord, " fire @ ", fire_coord)
print("bot1 mission:", mission_success_1)
print("bot2 mission:", mission_success_2)
print("bot3 mission:", mission_success_3)

# Open a file in append mode ('a')
with open('output5.txt', 'a') as file:
    file.write(f"q: {q:0.2f}, d: {d}, bot1: {mission_success_1}, bot2: {mission_success_2}, bot3: {mission_success_3}\n")
