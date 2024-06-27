# importing "heapq" to implement heap queue
import heapq
import sys

from create_ship_layout import init, create_ship_layout, open_dead_end, create_bot_fire_button
from create_ship_layout import create_dist_matrix, create_fire_matrix, update_fire_matrix, get_fire_neighbors
from utility import weight

# Define the directions for moving in the matrix
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
FIRE_PROBABILITY_THRESHOLD = 0.6

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
#print("ship layout:")
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

def print_path(parent, curr):
    complete_path = [curr]
    while curr in parent:
        curr = parent[curr]
        complete_path.append(curr)
    complete_path.reverse()
    print(complete_path)
    return

def heuristic_bot1(a, b):
    return round(abs(a[0] - b[0]) + abs(a[1] - b[1]), 2)

def heuristic_bot2(a, b, fire_matrix):
    d = len(fire_matrix)
    return round(heuristic_bot1(a,b)+(d*fire_matrix[a[0]][a[1]]), 2)

def heuristic_bot3(a, b, fire_matrix):
    d = len(fire_matrix)
    num_neighbors, combined_prob = get_fire_neighbors(ship_map, fire_matrix, d, d, a[0], a[1])
    return round(heuristic_bot1(a,b)+(d*combined_prob*num_neighbors), 2)

def a_star(ship_map, start, goal, fire_matrix, bot_num):
    myheap = []
    heapq.heappush(myheap, (0, start))
    parent = {}
    cost = {start : 0}
    est_total_cost = {start : heuristic_bot1(start, goal)}

    while myheap:
        curr_cell = heapq.heappop(myheap)
        if(fire_matrix[curr_cell[1][0]][curr_cell[1][1]] >= FIRE_PROBABILITY_THRESHOLD):
            print("bot and fire in the same cell. Mission fails!")
            return "false"
        
        if(curr_cell[1] == button_coord):
            print("bot finds button and puts off fire")
            print_path(parent, curr_cell)
            return "true"
    
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        print("processing i:", i, "j: ", j)
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)
        print("fire matrix")
        for f in range(0, len(fire_matrix)):
            print(fire_matrix[f])

        for x, y in DIRECTIONS:
            neighbor = (curr_cell[1][0]+x, curr_cell[1][1]+y)
            if (0 <= neighbor[0] < d and 0 <= neighbor[1] < d) and (ship_map[neighbor[0]][neighbor[1]] == 1): #ignores initial fire cell
                est_curr_cost = cost[curr_cell[1]]+1

                if neighbor not in est_total_cost or est_curr_cost < est_total_cost[neighbor]:
                    parent[neighbor] = curr_cell[1]
                    cost[neighbor] = est_curr_cost
                    if(bot_num == 1):
                        est_total_cost[neighbor] = est_curr_cost+heuristic_bot1(neighbor, goal)
                    elif(bot_num == 2):
                        est_total_cost[neighbor] = est_curr_cost+heuristic_bot2(neighbor, goal, fire_matrix)
                    else:
                        est_total_cost[neighbor] = est_curr_cost+heuristic_bot3(neighbor, goal, fire_matrix)
                    heapq.heappush(myheap, (est_total_cost[neighbor], neighbor))

        # Print the contents of the heap to verify
        print("Heap contents:")
        for item in myheap:
            print(item)
    return "false"
    
def run_bot(ship_map, bot_coord, button_coord, fire_coord, bot_num):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    return a_star(ship_map, bot_coord, button_coord, fire_matrix, bot_num)

'''
def run_bot2(ship_map, bot_coord, button_coord, fire_coord):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    return a_star(ship_map, bot_coord, button_coord, fire_matrix, 2)

def run_bot3(ship_map, bot_coord, button_coord, fire_coord):
    fire_matrix = create_fire_matrix(ship_map, fire_coord)
    return a_star(ship_map, bot_coord, button_coord, fire_matrix, 3)
'''
print("-----------------------------------------------------------------------------------------------")
mission_success_1 = run_bot(ship_map, bot_coord, button_coord, fire_coord, 1)
print("-----------------------------------------------------------------------------------------------")
mission_success_2 = run_bot(ship_map, bot_coord, button_coord, fire_coord, 2)
print("-----------------------------------------------------------------------------------------------")
mission_success_3 = run_bot(ship_map, bot_coord, button_coord, fire_coord, 3)
print("-----------------------------------------------------------------------------------------------")
print("Q is: ", q, " D is:", d)
print("bot @ ", bot_coord, " button @ ", button_coord, " fire @ ", fire_coord)
print("bot1 mission:", mission_success_1)
print("bot2 mission:", mission_success_2)
print("bot3 mission:", mission_success_3)

# Open a file in append mode ('a')
with open('out.txt', 'a') as file:
    file.write(f"q: {q:0.2f}, d: {d}, bot1: {mission_success_1}, bot2: {mission_success_2}, bot3: {mission_success_3}\n")
