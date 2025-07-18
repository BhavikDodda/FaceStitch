import sys
import json
from pyembroidery import EmbPattern, STITCH, END, write_dst

# handling

if len(sys.argv) != 3:
    print("Usage: python 5dstgen.py \"2points.json\" \"4path.json\"")
    sys.exit(1)
points_file = sys.argv[1]
path_file = sys.argv[2]

with open(points_file) as f:
    points = json.load(f)

with open(path_file) as f:
    path = json.load(f)

xs = [x for x, y in points]
ys = [y for x, y in points]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

width_dst = max_x - min_x
height_dst = max_y - min_y

width_cm = width_dst * 0.1 / 10  # from DST units to cm
height_cm = height_dst * 0.1 / 10

target_width=12.9
target_height=17.9

scale_factor = target_width/width_cm
scale_factor2 = target_height/height_cm
scale_factor=min(scale_factor,scale_factor2)
print(f"Bounding box: {(width_cm*scale_factor):.2f} cm x {(height_cm*scale_factor):.2f} cm")

# start

pattern = EmbPattern()

first = path[0]-1
pattern.add_stitch_absolute(STITCH, points[first][0] * scale_factor, points[first][1] * scale_factor)

# Add stitches
for i in path[1:]:
    x, y = points[i-1]
    pattern.add_stitch_absolute(STITCH, x * scale_factor, y * scale_factor)

pattern.add_command(END)

# Write to file
write_dst(pattern, "5output.dst")

print("Generated 5output.dst file")