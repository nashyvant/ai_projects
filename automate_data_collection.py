import subprocess

def float_range(start, end, step):
    while start < end:
        yield start
        start += step

#fixed grid size
#generate fixed grids
#fix the location of fire, bot, button
#run bot1 bot2 and bot3 and compare them so that you're making a fair comparison
'''
for q in float_range(0.1, 1, 0.1):
        if (q >= 0.1 and q <= 0.4) or q >= 0.95:
             for i in range(0, 10):
                 subprocess.run(["python", "main.py", str(q)])
        else:
             for i in range(0, 150):
                 subprocess.run(["python", "main.py", str(q)])
'''
#project 2
for alpha in float_range(0.1, 1, 0.1):
    for i in range(0, 100):
        subprocess.run(["python", "bot_finds_mouse.py", str(alpha)])

             
