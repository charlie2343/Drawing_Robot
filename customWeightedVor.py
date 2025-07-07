# !pseudocode: 
# Generate Centroidal Voronoi
#     create voronoi diagram
#     use shapely to change infinite cells to be bounded by canvas
#     compute centroids of all the cells
#     regenerate the cells 
#     clip that shit again 

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from geovoronoi import * 
from shapely.geometry import LineString, Polygon
from shapely.plotting import * 

#!!Create Image
from PIL import Image

cells = []
coord_limit = 400
# ## Level one header
img = Image.open("dragon.png").convert("L")  # "L" = grayscale
img = img.resize((coord_limit, coord_limit))                       # Resize to match domain
img_array = np.array(img)                          # Convert to NumPy array
img_array = 255 - img_array             # Invert so black = high weight
image_processed = Image.fromarray(img_array)
image_processed.show()
img_array = img_array / np.sum(img_array)          # Normalize for weighting
print(img_array)



from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from skimage.draw import polygon as sk_polygon
import matplotlib.image as mpimg

def get_weighted_centroid(cell, img_array):
    # Get pixel coordinates of polygon area
    x, y = cell.exterior.coords.xy
    rr, cc = sk_polygon(np.array(y), np.array(x), img_array.shape)

    if len(rr) == 0:
        return None

    values = img_array[rr, cc]  # pixel intensities (0–255)
    
    # Compute weighted centroid
    total_weight = np.sum(values)
    if total_weight == 0:
        return None
    
    weighted_x = np.sum(cc * values) / total_weight
    weighted_y = np.sum(rr * values) / total_weight

    return [weighted_x, weighted_y]


def generate_seeds(num_seeds, coord_limit): 
    points = []
   # print("Points datatype ", type(points))
   # points = np.array(points)
    for _ in range(num_seeds): 
        x = random.randint(0, coord_limit)
        y = random.randint(0, coord_limit)
        points.append([x, y])
    points, num_boundary_seeds = add_bounding_seeds(coord_limit=coord_limit, points_=points)
    return np.array(points), num_boundary_seeds
        
        
def add_bounding_seeds(coord_limit, points_): 
    if isinstance(points_, np.ndarray): 
        points_ = points_.tolist()
    new_points = points_
    offset = 20
    num_seeds = 20
    array = np.linspace(-offset,coord_limit + offset, num=num_seeds)
    boundary =[]
    for num in array: 
        #top
        boundary.append([num,0])
        #bottom
        boundary.append([num,coord_limit+offset])
        #left
        boundary.append([0,num])
        #right
        boundary.append([coord_limit + offset, num])
    for element in boundary: 
        new_points.append(element)
    return np.array(new_points), len(boundary)


    
    return np.array(points)
num_seeds = 1000
seeds, num_boundary_seeds = generate_seeds(num_seeds, coord_limit)
print("expected number of invalid cells (num boundary seeds)", num_boundary_seeds)
print(seeds)
print("seeds ", seeds)
vor_diagram = Voronoi(seeds)
print(vor_diagram)

# fig, ax = plt.subplots()
# ax.scatter(seeds[:, 0], seeds[:, 1], color='blue', marker=".")
# ax.set_title("Seed Points")
# ax.set_aspect('equal')
# ax.set_xlim(-20, 120)  # Set x-axis limits
# ax.set_ylim(-20, 120)  # Set y-axis limits


 
bounding_box = Polygon([(0,0), (coord_limit,0), (coord_limit,coord_limit), (0,coord_limit)])

#? Clip Voronoi regions to the bounding box
global count
count = 0
def bounded_voronoi_cell(i, vor, bounding_box):
    global count
    # print(f"Vor.point_region: {vor.point_region}")
    region_index = vor.point_region[i]
    region = vor.regions[region_index]

    if -1 in region or len(region) == 0:
        count += 1
        #print(f"Region {i} is invalid or infinite: {region}")
        # Infinite or invalid region
        return None

    polygon = [vor.vertices[v] for v in region]
    poly = Polygon(polygon)

    # Clip the polygon to the bounding box
    clipped = poly.intersection(bounding_box)
    if clipped.is_empty: 
        print("clipped.is_empty")
        return None
    else: 
        return clipped
    #return clipped if not clipped.is_empty else None


def find_centroid(polygon):
    if polygon.is_empty or not polygon.is_valid:
        return None
    p = polygon.centroid
    return [p.x, p.y]

def relax_voronoi(iterations, vor, bounding_box, input_seeds): 
    inner_seeds = input_seeds[:num_seeds]
    invalid_count = 0 
    invalid_weighted_centroid_count = 0 
    global cells 
    for _ in range(0, iterations):
        cells = []
        new_seeds = []
        for i in range(len(vor.points) - num_boundary_seeds):
            #! go through all seeds in the boundary box, get weighted centroids and append to new seeds, finally add bounding seeds
            poly = bounded_voronoi_cell(i, vor, bounding_box)
            if poly:
                # print("yay", i)
                # new_seeds.append(find_centroid(polygon=poly))
                wc = get_weighted_centroid(cell=poly, img_array=img_array)
                if wc != None: 
                    new_seeds.append(wc)
                else: 
                    invalid_weighted_centroid_count +=1 
                cells.append(poly)
            else: 
                invalid_count += 1
        #print(f"cells: {cells}")
        #for idx, polygon in enumerate(cells): 
        # print(f"Cells length: {len(cells)}")
        # print("seeds length: ", len(seeds))
        # print(type(new_seeds))
        # print("testing new seeds[0] ", new_seeds[0])
        print("invalid_weighted_centroid_count: ", invalid_weighted_centroid_count)
        new_with_bounding_seeds,asd = add_bounding_seeds(coord_limit=coord_limit, points_=new_seeds)
        vor = Voronoi(new_with_bounding_seeds)

    print("Invalid polys during relaxation ", invalid_count )
    
    return vor
    print(f"region count: {count}")
    print("cells: ", cells)

newCentroidalVoronoi = relax_voronoi(5,vor=vor_diagram, bounding_box=bounding_box, input_seeds=seeds)

# invalid_count = 0 
# for i in range(len(newCentroidalVoronoi.points)):
#     poly = bounded_voronoi_cell(i, newCentroidalVoronoi, bounding_box)
#     invalid_count += 1
#     if poly:
#         cells.append(poly)
#print(f"cells: {cells}")

print(f"region count: {count}")
#print("cells: ", cells)
# print("Invalid Cells: ", invalid_count)
newCentroidalVoronoi2 = relax_voronoi(30,vor=vor_diagram, bounding_box=bounding_box, input_seeds=seeds)

# print("Cells: ", cells)

fig, ax = plt.subplots()
ax.clear()
for polygon in cells: 
    plot_polygon(polygon, ax=ax, add_points=False, color=(random.random(),random.random(),random.random()), alpha=0.5)
    #plt.plot(list(polygon.centroid))
    plt.scatter(polygon.centroid.x, polygon.centroid.y, s=1)
    
ax.set_aspect('equal')
ax.set_xlim(-0, coord_limit)
ax.set_ylim(-0, coord_limit)



ax.set_title("Centroidal Voronoi Polygons")
#voronoi_plot_2d(vor_diagram)
voronoi_plot_2d(newCentroidalVoronoi, show_points = False, show_vertices =False)
voronoi_plot_2d(vor_diagram, show_points = False, show_vertices =False)
voronoi_plot_2d(newCentroidalVoronoi2,show_points=False, show_vertices =False)
#Create Voronoi diagram using scipy.spatial
#voronoi_plot_2d(vor_diagram, ax)
ax.imshow(img, extent=[-0, coord_limit, -0, coord_limit],  cmap='gray')
plt.show()
# print(vor_diagram)

# print("Voronoi regions", vor_diagram.regions)
# print("Voronoi ridges", vor_diagram.ridge_vertices)

# neg_vertices = [v for v in vor_diagram.ridge_vertices if -1 in v]
# print(f"Negative vertices: {neg_vertices}")