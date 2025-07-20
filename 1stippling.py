import os
import sys
cmd = sys.executable

# The filename of the image you want to stipple goes here.
ORIGINAL_IMAGE = "input/gap_edited.jpg"

# Total number of points to stipple your image with
NUMBER_OF_POINTS = 10000


full_command = f" weighted-voronoi-stippler/stippler.py {ORIGINAL_IMAGE} --json --save --n_point {NUMBER_OF_POINTS}"

os.system(cmd + full_command)