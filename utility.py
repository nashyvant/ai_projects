import math
import random

def sample_bit(p):
    if random.random() <= p :
        return 1
    else:
        return 0