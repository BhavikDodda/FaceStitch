import json

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
