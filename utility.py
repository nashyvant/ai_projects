import math 
def weight(d):
    print("weight fn: d is: ", d)
    count = 0
    orig_d = d
    d = int(d)
    while(int(d)):
        print(d)
        d = d/10
        count += 1
    #design choice, adding weights to the fire matrix
    #weight for the fire matrix would be to multiple probability with the number of digits
    max_dist = math.sqrt(orig_d*orig_d+orig_d*orig_d)
    print("weight is: ", count*10)
    return count*10*max_dist