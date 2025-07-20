# Goal

To convert an image into an embroidery using a single continuous line.

Example: 

<img width="152" height="152" alt="image" src="https://github.com/user-attachments/assets/41920208-dc46-4758-be36-5ce3bd47db48" />

## Inspiration

This project is inspired by the Mona Lisa TSP Challenge: https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html

# Procedure

1. Convert the image into a list of points. This process is calling **stippling**. Types:
   - MacQueen Tractor Beam Stippling
   - Weighted Voronoi Stippling
2. Apply the [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) algorithm on the list of points to find the path/route through them.

Since TSP is an NP-hard problem, this means that it's very computationally expensive and we would therefore need to use a heuristic algorithm. Here, we'll use the [LKH](https://en.wikipedia.org/wiki/Lin%E2%80%93Kernighan_heuristic) algorithm which finds a sub-optimal solution (path).
This is good enough for our use case.

# Execute

In your cmd terminal run the following command to clone this repository:

```cmd
git clone https://github.com/BhavikDodda/FaceStitch.git
```

## Manual Method

1. Save your image in the `input` folder.
2. Set `ORIGINAL_IMAGE` in `1stippling.py` to the file path of the image from step 1, and execute it to generate the stippling points which will be exported to `2points.json`.
3. Now to generate a .tsp file from 2points.json, execute `3gentsp.py`. This will create `cities.tsp` in the root of the same folder.
4. The `cities.tsp` file can be used to compute the LKH route through the points/cities. Two methods:
   - Run `4lkhpy.py` to generate `4path.json` containing the LKH route.
   - (OR) Open the `cities.tsp` file on [Concorde](https://www.math.uwaterloo.ca/tsp/concorde/index.html), go to `Heuristics` and select 'Lin Kernighan' to compute the path. To export the path: File->Save Tour.
5. To stitch the image on [Brother sewing machine](https://www.brother.in/en/sewing-machines) you would need a .dst file. In cmd, running `python 5dstgen.py "2points.json" "4path.json"` generates a `5output.dst` which can be imported to the stitching machine.

## Faster Method

This relies on the Node.js+Flask website created to generate the stippling, LKH path and .dst file. It's therefore limited to what I've incorported.

- First run the following to enable the backend server
```cmd
python backend/app.py
```
- Open another terminal in the same root and run this parallelly for the site
```cmd
node frontend/server.js
```
You should see the following message:
`Server running on http://localhost:3000`

- Now visit `http://localhost:3000`, upload your image, choose one of the Stippling algorithms, calculate the route, and finally download the .dst file!

(If you don't see the output right away, make sure to wait a couple of minutes before each step)

### Output

<img width="418" height="452" alt="image" src="https://github.com/user-attachments/assets/83aad06a-4124-46f8-8c8a-a3fe74c1a697" /> <img width="420" height="454" alt="image" src="https://github.com/user-attachments/assets/1e39080c-e930-4fa9-bbf9-b2c126c2aa65" />




# Additional Comments

The site is still under development, so feel free to contribute to the project!

# Resources

- "Opt Art: From Mathematical Optimization to Visual Design" book by Robert Bosch
- Concorde Solver
