import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
# from shapely.geometry import Polygon
# from geovoronoi import voronoi_regions_from_coords
# from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

# # ----------------------------------
# # Parameters
# num_seeds = 100
# canvas_size = 100
# num_iterations = 10
# # ----------------------------------

# # Step 1: Generate random seeds
# def generate_seeds(n, coord_limit):
#     return np.array([[random.uniform(0, coord_limit), random.uniform(0, coord_limit)] for _ in range(n)])

# # Step 2: Define bounding canvas (square)
# bounding_box = Polygon([(0, 0), (canvas_size, 0), (canvas_size, canvas_size), (0, canvas_size)])

# # Step 3: Lloyd Relaxation
# seeds = generate_seeds(num_seeds, canvas_size)

# for iteration in range(num_iterations):
#     # Generate Voronoi diagram and clip to bounding box
#     region_polys, region_pts = voronoi_regions_from_coords(seeds, bounding_box)

#     # Compute centroids
#     centroids = []
#     for poly in region_polys.values():
#         if poly.is_empty or not poly.is_valid:
#             continue
#         centroid = poly.centroid
#         centroids.append([centroid.x, centroid.y])

#     seeds = np.array(centroids)

# # Step 4: Final Plot
# fig, ax = subplot_for_map(figsize=(8, 8))
# plot_voronoi_polys_with_points_in_area(ax, region_polys, seeds, region_pts)
                                       
# ax.set_title(f"Lloyd's Relaxation with {num_iterations} Iterations")
# plt.show()

import numpy as np
import random
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.plotting import plot_polygon
from geovoronoi import voronoi_regions_from_coords
from scipy.spatial import Voronoi, voronoi_plot_2d

# -- Config --
canvas_size = 100
num_seeds = 5
num_iterations = 10

# -- Bounding box polygon --
bounding_box = Polygon([(0, 0), (canvas_size, 0), (canvas_size, canvas_size), (0, canvas_size)])

# -- Generate random seed points --
def generate_seeds(n, limit):
    return np.array([[random.uniform(0, limit), random.uniform(0, limit)] for _ in range(n)])

# seeds = generate_seeds(num_seeds, canvas_size)
# print(seeds)

seeds = [[54.79446724, 15.48425111],
 [62.82897817, 84.90680576],
 [66.31224021, 16.59197943],
 [33.695472,   90.60822425],
 [80.75228078, 10.26000975]]
 
vor = Voronoi(seeds)
# print(f"regions:{ vor.regions}")
# print(f"ridge vertices: {vor.ridge_vertices}")
# perp_seeds = vor.ridge_points
# #print(perp_seeds)
# # print(f"ridge points: {perp_seeds}")
# # print(f"Perpendicular bisector seed coordinates: Seed1: {vor.vertices[perp_seeds[0]]} Seed2: {vor.vertices[perp_seeds[1]]}")
# print(f"Test perp seed: {perp_seeds[0]}")
# print(vor.vertices)
# print("test penis", vor.vertices[perp_seeds[0]])

for idx,vertex in enumerate(vor.ridge_vertices): 
    print(vertex)
    # coordinates of the ridge_vertices
    c1 = vor.vertices[vertex[0]]
    c2 = vor.vertices[vertex[1]]
    print(f"ridge between {c1} and {c2}")
    point_idx = vor.ridge_points[idx]
    print(f'ridge points: {point_idx} penis')
    p1_coord = vor.points[point_idx[0]]
    p2_coord = vor.points[point_idx[1]]
    print(f"Perp bisector between coords of point 1: {p1_coord} and point 2: {p2_coord}")
    direction = p2_coord - p1_coord
    normal = np.array([-direction[1], direction[0]], dtype=float)  # perpendicular
    normal /= np.linalg.norm(normal)
    
    if -1 in (v1, v2):
            # Infinite edge — extend it in the direction of its normal
            if v1 == -1:
                finite_vertex = v2
            else:
                finite_vertex = v1


voronoi_plot_2d(vor)
plt.show()
    
# # # -- Lloyd Relaxation Loop --
# for _ in range(num_iterations):
#     region_polys, region_pts = voronoi_regions_from_coords(seeds, bounding_box)
#     centroids = []
#     for poly in region_polys.values():
#         if not poly.is_empty and poly.is_valid:
#             centroids.append([poly.centroid.x, poly.centroid.y])
#     seeds = np.array(centroids)

# # -- Plotting manually using shapely + matplotlib --
# import matplotlib.pyplot as plt
# from descartes import PolygonPatch

# fig, ax = plt.subplots(figsize=(8, 8))
# for poly in region_polys.values():
#     if not poly.is_empty:
#         patch = PolygonPatch(poly, fc='skyblue', ec='black', alpha=0.6)
#         ax.add_patch(patch)

# ax.scatter(seeds[:, 0], seeds[:, 1], color='red', s=5)
# ax.set_xlim(0, canvas_size)
# ax.set_ylim(0, canvas_size)
# ax.set_aspect('equal')
# ax.set_title(f"Centroidal Voronoi (Lloyd's Relaxation x{num_iterations})")
# plt.show()
