# from shapely.geometry import Polygon
# from shapely.plotting import plot_polygon
# from matplotlib import pyplot as plt
# # canvas_size = 100
# # fig, ax = plt.subplots(figsize=(8, 8))
# # ax.set_ylim(-10, canvas_size + 10)
# # ax.set_xlim(-10, canvas_size + 10)

# polygon = Polygon([(0, 0), (20, 0), (40, 30), (50, 60), (40, 70)])
# print(f"shapely polygon centoid {polygon.centroid}")
# # plot_polygon(polygon, edgecolor='black', facecolor='none')
# # def find_centroid(polygon):
# #     if polygon.is_empty or not polygon.is_valid:
# #         return None
# #     return polygon.centroid

# # def custom_centroid(polygon): 
# #     if polygon.is_empty or not polygon.is_valid:
# #         return None
    
# # centroid = find_centroid(polygon)
# # print("Centroid:", centroid)
# # print("Polygon vertices: ", list(polygon.exterior.coords))
# # plt.show()

# for idx, element in enumerate(["apple", "penis", "puppies"]): 
#     print(f"Index: {idx} /n Element: {element}")

import numpy as np

arr = np.array([1, 2, 3])
my_list = [4, 5]
new_arr = np.append(arr, my_list)
print(new_arr)