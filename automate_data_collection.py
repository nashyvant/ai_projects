import subprocess

def float_range(start, end, step):
    while start < end:
        yield start
        start += step

for q in float_range(0.1, 1.01, 0.1):
    for d in range(40, 50):
        for i in range(0, 10):
            subprocess.run(["python", "main.py", str(d), str(q)])
