# importing "heapq" to implement heap queue
import heapq
import sys
import copy

from create_ship_layout import init, create_ship_layout, open_dead_end, create_bot_fire_button
from create_ship_layout import create_fire_matrix, simulate_fire_matrix, update_fire_matrix
#from utility import weight
from utility import get_path

from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the date and time as a string
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

# Print the current date and time
print("Current Date and Time:", current_time)

# Define the directions for moving in the matrix
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

'''
d = input("Enter row or column size D?")
d = int(d)
q = input("Enter q between 0 and 1, defining flammability of the ship?")
q = float(q)
'''
#project 1 - bot turns off fire
# init the 2D map of ship
if len(sys.argv) != 2:
    print("Usage: python main.py <float_arg>")

# Retrieve command-line arguments
#d = 40 #fixed grid size
d = 21
q = float(sys.argv[1])

MAX_ITERATIONS = d*d*2

print("Automating for q: ", q, " d: ", d)

#ship_map = init(d)
#create_ship_layout(ship_map)
#open_dead_end(ship_map)

ship_map = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

#bot_coord, button_coord, fire_coord = create_bot_fire_button(ship_map)
fire_coord = (0, 11)
bot_coord = (9, 0 )
button_coord = (17, 17)  

ship_map[fire_coord[0]][fire_coord[1]] = -1

print("ship layout with init fire cell:")
for i in range(0, len(ship_map)):
    print(ship_map[i])

print("bot @ ", bot_coord, " button @ ", button_coord, " fire @ ", fire_coord)

rows = len(ship_map)
cols = len(ship_map[0])

def heuristic(a, b):
    return round((abs(a[0] - b[0]) + abs(a[1] - b[1])), 2)

def a_star(ship_map, start, goal, fire_matrix, bot_num):
    myheap = []
    heapq.heappush(myheap, (0, start))
    parent = {}
    cost = {start : 0}
    est_total_cost = {start : heuristic(start, goal)}
    prev_cell = ()
    loop_count = 0
    if(bot_num == 3): #simulate adjacent fire cells
        sim_fire_matrix = simulate_fire_matrix(ship_map, fire_matrix, q, 1)
    
    while myheap:
        curr_cell = heapq.heappop(myheap)
        if(curr_cell == prev_cell):
            continue
        
        if(curr_cell[1] == button_coord):
            #print("bot finds path to button! ")
            return get_path(parent, curr_cell[1])
    
        i = curr_cell[1][0]
        j = curr_cell[1][1]
        #print("processing i:", i, "j: ", j)

        for x, y in DIRECTIONS:
            neighbor = (curr_cell[1][0]+x, curr_cell[1][1]+y)
            if (0 <= neighbor[0] < d and 0 <= neighbor[1] < d) and (ship_map[neighbor[0]][neighbor[1]] == 1): #ignores fire and block cells
                if(bot_num == 1 or bot_num == 2):
                    est_curr_cost = cost[curr_cell[1]]+1
                else:
                    if(sim_fire_matrix[neighbor[0]][neighbor[1]] == 0): #bot_num3 avoids potential future fire cells
                        est_curr_cost = cost[curr_cell[1]]+1
                    else:
                        continue

                if neighbor not in cost or est_curr_cost < cost[neighbor]:
                    parent[neighbor] = curr_cell[1]
                    cost[neighbor] = est_curr_cost
                    est_total_cost[neighbor] = est_curr_cost+heuristic(neighbor, goal)
                    heapq.heappush(myheap, (est_total_cost[neighbor], neighbor))
                    #print("neighbor:", neighbor, "est curr and total cost of neighbor is: ", est_curr_cost, est_total_cost[neighbor])

        print(myheap)
        prev_cell = curr_cell
        loop_count += 1
    return None
    
def run_bot(ship_map, bot_coord, button_coord, fire_coord, bot_num):
    fire_matrix = create_fire_matrix(len(ship_map), fire_coord)
    while( True):
        path, steps = a_star(ship_map, bot_coord, button_coord, fire_matrix, bot_num)
        if path is None:
            if(bot_num == 3): # try again by avoiding only current fire cells for bot #3
                print("BOT_NUM 3; No Path. Try only with current fire cells!")
                path = a_star(ship_map, bot_coord, button_coord, fire_matrix, 2) # which is the same as running bot2
                if path is None:
                    print("No Path. Fire has spread to the button cell or bot cell! ")
                    return 0
                else:
                    print(f"Path to button: {path}")
            else:
                print("Fire has spread to the button cell or bot cell!")
                return 0
        else:
            print(f"Path to button: {path}")

        if bot_coord != button_coord:
            bot_coord = path[1] #move to the next position in a_star

        print("bot is now at:", bot_coord)

        if bot_coord == button_coord:
            print("bot turned off fire")
            return 1
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)

        if ship_map[bot_coord[0]][bot_coord[1]] == -1:
            print("bot on fire!")
            return 0
        
        if ship_map[button_coord[0]][button_coord[1]] == -1:
            print("button on fire!")
            return 0
        
def run_bot1(ship_map, bot_coord, button_coord, fire_coord, bot_num):
    fire_matrix = create_fire_matrix(len(ship_map), fire_coord)
    path = a_star(ship_map, bot_coord, button_coord, fire_matrix, bot_num)
    if path is None:
        print("Fire has spread to the button cell or bot cell!")
        return 0
    else:
        print(f"Path to button: {path}")

    i = 1
    while(True and i < len(path)):
        if bot_coord != button_coord:
            bot_coord = path[i] #move to the next position in a_star

        print("bot is now at:", bot_coord)

        if bot_coord == button_coord:
            print("bot turned off fire")
            return 1
        
        fire_matrix = update_fire_matrix(ship_map, fire_matrix, q)

        if ship_map[bot_coord[0]][bot_coord[1]] == -1:
            print("bot on fire!")
            return 0
        
        if ship_map[button_coord[0]][button_coord[1]] == -1:
            print("button on fire!")
            return 0
        
        i += 1
        
print("----------------------BOT1---------------------------------------------------------------------")
backup_ship_map = copy.deepcopy(ship_map)
mission_success_1 = run_bot1(ship_map, bot_coord, button_coord, fire_coord, 1)
print("----------------------BOT2---------------------------------------------------------------------")
ship_map = copy.deepcopy(backup_ship_map) #restore original ship layout
mission_success_2 = run_bot(ship_map, bot_coord, button_coord, fire_coord, 2)
print("----------------------BOT3---------------------------------------------------------------------")
ship_map = copy.deepcopy(backup_ship_map) #restore original ship layout
mission_success_3 = run_bot(ship_map, bot_coord, button_coord, fire_coord, 3)
print("-----------------------------------------------------------------------------------------------")
print("Q is: ", q, " D is:", d)
print("bot @ ", bot_coord, " button @ ", button_coord, " fire @ ", fire_coord)
print("bot1 mission:", mission_success_1)
print("bot2 mission:", mission_success_2)
print("bot3 mission:", mission_success_3)
print("-----------------------------ALL DONE----------------------------------------------------------")
# Open a file in append mode ('a')
with open('out.txt', 'a') as file:
    file.write(f"q: {q:0.2f}, d: {d}, bot1: {mission_success_1}, bot2: {mission_success_2}, bot3: {mission_success_3}\n")
