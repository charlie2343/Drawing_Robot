# create randomly distributed points on the plane

# calculate the voronoi cells for each of the points: 
#     How am I going to create a set of points that represent the voronoi cells? or create boundaries for it?? 
    
# find centroids of voronoi
#     integrate to find total area
#     find weighted sum x direction 
#     weighted x / total area
#     x coord com = x max 

# !pseudocode: 
# Generate Centroidal Voronoi
#     create voronoi diagram
#     use shapely to change infinite cells to be bounded by canvas
#     compute centroids of all the cells
#     regenerate the cells 
#     clip that shit again 
    
    
import numpy as np
import random

def generate_seeds(num_seeds, coord_limit): 
    points = []
    for _ in range(num_seeds): 
        x = random.randint(0, coord_limit)
        y = random.randint(0, coord_limit)
        points.append([x, y])
    points = np.array(points)
    print(points)
    return points
    
points = generate_seeds(10, 100)
# points = np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
#                    [2, 0], [1.4, 1], [2, 2]])
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(points)
print(vor)

def polygon_centroid(vertices):
    """
    Compute centroid of a polygon using the shoelace formula.
    """
    x = vertices[:, 0]
    y = vertices[:, 1]
    area = 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])
    Cx = (1/(6*area)) * np.sum((x[:-1] + x[1:]) * (x[:-1]*y[1:] - x[1:]*y[:-1]))
    Cy = (1/(6*area)) * np.sum((y[:-1] + y[1:]) * (x[:-1]*y[1:] - x[1:]*y[:-1]))
    return np.array([Cx, Cy])

# Step 3: Compute centroids
centroids = []
unbounded_count = 0
for point_idx, region_idx in enumerate(vor.point_region):
    region = vor.regions[region_idx]
    print(region)
    if -1 in region or len(region) == 0:
        # Skip infinite or invalid regions
        unbounded_count += 1
        continue
    print("Invalid count: ", unbounded_count)
    polygon = np.array([vor.vertices[i] for i in region + [region[0]]])  # close polygon
    centroid = polygon_centroid(polygon)
    centroids.append(centroid)

centroids = np.array(centroids)
##!I want the centroids
print(centroids)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 6))

from shapely.geometry import LineString, Polygon

#create funciton that finds intersections and recreates the voronoi diagram

def construct_finite_voronoi_cell(region, vertices, bbox_poly):
    """Construct finite polygon for a Voronoi region (clip to bbox if needed)."""
    if -1 in region or len(region) == 0:
        return None  # infinite or degenerate

    poly_points = [vertices[i] for i in region]
    poly = Polygon(poly_points)
    if not poly.is_valid:
        poly = poly.buffer(0)  # fix self-intersections if needed

    clipped_poly = poly.intersection(bbox_poly)
    return clipped_poly if not clipped_poly.is_empty else None

finite_polys = []
bounding_box = Polygon([(0,0), (100,0), (100,100), (0,100)])
for point_idx, region_idx in enumerate(vor.point_region):
    region = vor.regions[region_idx]
    clipped = construct_finite_voronoi_cell(region, vor.vertices, bounding_box)
    if clipped:
        finite_polys.append(clipped)
print("length of finite polys", len(finite_polys))
        
        

# 4. Draw Voronoi edges, clipped to bounding box
for vpair in vor.ridge_vertices:
    if -1 in vpair:
        # Skip infinite ridges for now or handle with custom logic
        continue
    p1, p2 = vor.vertices[vpair]
    line = LineString([p1, p2])
    clipped = line.intersection(bounding_box)
    if not clipped.is_empty:
        x, y = clipped.xy
        ax.plot(x, y, 'k-')


fig = voronoi_plot_2d(vor)
plt.show()

#I created random points and a voronoi diagram. Now I want to relax their seeds to their centroids