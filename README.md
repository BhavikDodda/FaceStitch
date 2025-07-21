# FaceStitch

Transform images into beautiful embroidery designs using a single continuous line.

## Inspiration

This project is inspired by the [Mona Lisa TSP Challenge](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html)

## Overview

**FaceStitch** converts an image into a list of points (stippling), then finds an optimal or near-optimal path through those points using the Lin Kernighan Heuristic (LKH). The result can be plotted or stitched as a single continuous line, perfect for embroidery machines.

Example: 

<img width="152" height="152" alt="image" src="https://github.com/user-attachments/assets/41920208-dc46-4758-be36-5ce3bd47db48" />

## How It Works

1. **Image to Points (Stippling):**  
   The image is processed to extract feature points using either MacQueen Tractor Beam Stippling or Weighted Voronoi Stippling.

2. **Route Optimization (TSP):**  
   The [LKH algorithm](https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic) is employed to find an efficient route through the points, minimizing total distance.

3. **Embroidery Output:**  
   The computed path is exported in a format compatible with [embroidery machines](https://www.brother.in/en/sewing-machines) (e.g., `.dst` file).

## Getting Started

Clone the repository:

```bash
git clone https://github.com/BhavikDodda/FaceStitch.git
```

### **Manual Method**

1. **Prepare Image:**
   - Save your image in the `input` folder.

2. **Stippling:**
   - Set `ORIGINAL_IMAGE` in `1stippling.py` to the image path, then run the script to produce `2points.json`.

3. **TSP Conversion:**
   - Run `3gentsp.py` to convert `2points.json` into `cities.tsp`.

4. **Calculate Path:**
   - Option 1: Run `4lkhpy.py` to generate `4path.json` (the LKH route).
   - Option 2: Use [Concorde Solver](https://www.math.uwaterloo.ca/tsp/concorde/index.html). Load `cities.tsp`, choose 'Lin Kernighan' under Heuristics, and export the path via File → Save Tour.

5. **Create Embroidery File:**
   - Run the following command to generate a `.dst` file for your stitching machine:
   ```bash
   python 5dstgen.py "2points.json" "4path.json"
   # Output: 5output.dst
   ```

### **Faster Web-Based Method**

*This method requires Node.js and Flask.*

1. Start the backend server:

   ```bash
   python backend/app.py
   ```

2. In a new terminal, start the frontend server:

   ```bash
   node frontend/server.js
   ```

3. Open your browser and visit [http://localhost:3000](http://localhost:3000).

4. Upload your image and process it via the web interface to obtain the `.dst` file.

> **Tip:** Wait a minute between steps if the output does not appear immediately.

### Output

<img width="418" height="452" alt="image" src="https://github.com/user-attachments/assets/83aad06a-4124-46f8-8c8a-a3fe74c1a697" /> <img width="420" height="454" alt="image" src="https://github.com/user-attachments/assets/1e39080c-e930-4fa9-bbf9-b2c126c2aa65" />

## Resources

- "Opt Art: From Mathematical Optimization to Visual Design" by Robert Bosch
- [Concorde TSP Solver](https://www.math.uwaterloo.ca/tsp/concorde/index.html)

## Contributing

The site and code are under active development! Contributions, feature requests, and ideas are welcome. Feel free to open an issue or a pull request.
