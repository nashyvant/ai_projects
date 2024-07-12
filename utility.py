import math
import random

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