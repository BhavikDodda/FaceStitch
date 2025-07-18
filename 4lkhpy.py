import subprocess

with subprocess.Popen(
    ["LKH-2.exe", "example.par"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
) as proc:
    try:
        for line in proc.stdout:
            print(line, end='')
            if "Time.total" in line:
                print("\nDetected 'Time.total'—terminating process.")
                proc.terminate() 
                break
    except KeyboardInterrupt:
        proc.terminate()
    finally:
        if proc.poll() is None:
            proc.kill()
print("DONE")

path = []

with open("example.tour", "r") as f:
    inside_tour_section = False
    for line in f:
        line = line.strip()
        if line == "TOUR_SECTION":
            inside_tour_section = True
            continue
        if inside_tour_section:
            if line == "-1":
                break
            path.append(int(line))

# Save to 4path.json
import json
with open("4path.json", "w") as f:
    json.dump(path, f)
