import subprocess

def float_range(start, end, step):
    while start < end:
        yield start
        start += step

for q in float_range(0.1, 1.01, 0.1):
    for d in range(2, 51):
        for i in range(0, 3):
            subprocess.run(["python", "main.py", str(d), str(q)])
