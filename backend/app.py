from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os
import json
import numpy as np
import random
import subprocess
from scipy.spatial import KDTree
from pyembroidery import EmbPattern, STITCH, END, write_dst

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    # Convert to grayscale
    img = Image.open(filepath).convert('L')
    img = img.resize((500, 500))
    pixels = np.array(img)

    # Generate stippling points based on intensity
    k = 10000  # number of darts

    # Flatten image and create weights
    height, width = pixels.shape
    all_coords = [(x, y) for y in range(height) for x in range(width)]
    weights = [255 - pixels[y, x] for (x, y) in all_coords]

    # throw k darts weighted by darkness
    points = random.choices(all_coords, weights=weights, k=k)
    tree = KDTree(points)
    ni = [0] * k

    for _ in range(1000):
        w = random.choices(all_coords, weights=weights, k=1)[0]
        _, closest_idx = tree.query(w)

        
        # Update n_i and drag point towards w
        ni[closest_idx] += 1
        n=ni[closest_idx]
        px, py = points[closest_idx]
        new_x = (1 / (n + 1)) * w[0] + (n / (n + 1)) * px
        new_y = (1 / (n + 1)) * w[1] + (n / (n + 1)) * py
        points[closest_idx] = (new_x, new_y)

        tree = KDTree(points)
        
        
    print(len(points))
    # scalefactor=500/(height if height>width else width)
    # points=[[pt[0]*scalefactor,pt[1]*scalefactor] for pt in points]
    # Save to JSON
    with open('2points.json', 'w') as f:
        json.dump(points, f)

    # Clear the upload folder
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    return jsonify(points)

@app.route('/calculate-route', methods=['POST'])
def calculate_route():
    
    # Load points from JSON
    with open("2points.json", "r") as f:
        points = json.load(f)

    # Write to cities.tsp
    with open("cities.tsp", "w") as f:
        f.write("NAME: cities\n")
        f.write("TYPE: TSP\n")
        f.write(f"COMMENT: {len(points)}-city problem\n")
        f.write(f"DIMENSION: {len(points)}\n")
        f.write("EDGE_WEIGHT_TYPE: EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")

        for idx, (x, y) in enumerate(points, 1):  # 1-based indexing
            f.write(f"{idx} {x} {y}\n")

        f.write("EOF\n")


##

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
    with open("4path.json", "w") as f:
        json.dump(path, f)

    ##
    return jsonify({"points":points,"path":path})

from flask import send_file
@app.route('/download-dst', methods=['GET'])
def download_dst():
    points_file = "2points.json"
    path_file = "4path.json"

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
    write_dst(pattern, "backend/5output.dst")

    print("Generated 5output.dst file")



    return send_file('5output.dst', as_attachment=True)

if __name__ == '__main__':
    app.run()