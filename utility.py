import math 
def weight(d):
    orig_d = int(d)
    #design choice, adding weights to the fire matrix
    #weight for the fire matrix would be to multiple probability with the number of digits
    max_dist = math.sqrt(orig_d*orig_d+orig_d*orig_d)
    return round(max_dist*10, 2) # *10 helps add more weight to the fire values  

def neighbor_weight(d):
    orig_d = int(d)
    #design choice, adding weights to the fire matrix
    #weight for the fire matrix would be to multiple probability with the number of digits
    max_dist = math.sqrt(orig_d*orig_d+orig_d*orig_d)
    return round(max_dist*10, 2) # *10 helps add more weight to the fire values  
