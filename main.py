# 1. Import Libraries
from PIL import Image     # Pillow for image processing
import numpy as np   # NumPy for fast matrix math
import math    # For trig functions
import serial  # Optional: to send via serial

# 2. Load and Preprocess Image
img = Image.open("tiger.jpg")
new_width = 1000
new_height = int(img.height * (new_width / img.width))  # Maintain aspect ratio
print(f"Original size: {img.size}, New size: {new_width}x{new_height}")
img = img.resize((new_width, new_height))
img = img.convert("L")  # Convert to grayscale
img.show()

pixel_array = np.array(img, dtype=float)  # Convert to NumPy array
print(f"Pixel array shape: {pixel_array.shape}")
print(pixel_array)

# loop through the pixel array rows: 
#     loop through the pixel array columns:
# #     pixel_value = pixel_array[row, col]
# white_distance = 255 - pixel_value  # Assuming white is 255, black is 0
# black_distance = pixel_value  # Assuming black is 0, white is 255
# if white_distance < black_distance:
#     draw stipple
# else: 
#     move to next pixel
    
# error = original value - new quantized value
# distribute_error(pixel_array, row, col, error)

for row in range(0,pixel_array.shape[0]): 
    for col in range(0,pixel_array.shape[1]):
        pixel_value = pixel_array[row, col]
        error = 0
        white_distance = 255 - pixel_value
        if white_distance > pixel_value: 
            #drawstipple() # do i just change the pixel value or shoudl I draw a circle? 
            error = pixel_value
            pixel_array[row, col] = 0 
        else: 
            error = pixel_value -255
            pixel_array[row, col] = 255
        try:
            if col != 0:
                pixel_array[row+1, col-1] += error * 3/16 
            pixel_array[row, col+1] += error * 7/16
            pixel_array[row+1, col] += error * 5/16
            pixel_array[row+1, col+1] += error * 1/16
        except IndexError:
            pass
        
print(pixel_array)
# distribute error
# check if pixel is not at col[0] or row pixel_array.shape[0] -1: 
final_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
final_image = Image.fromarray(final_array)
final_image.show()
final_image.save("tiger_dithered.jpg")
    


# empty_array = np.zeros((100, 100))
# #print(empty_array)
# for row in range(0,empty_array.shape[0]): 
#     for col in range(0,empty_array.shape[1]):
#         # if col ==0: 
#         #     pass
#         # elif col ==empty_array.shape[1]-1: 
#         #     pass
        
#         try:
#             if col != 0: 
#                 empty_array[row+1, col-1] += 1 * 3/16
#             empty_array[row, col+1] += 1 * 7/16
#             empty_array[row+1, col] += 1 * 5/16
#             empty_array[row+1, col+1] += 1 * 1/16
#         except IndexError:
#             empty_array[row, col] = 0
#             pass
#         if col == 0: 
#             empty_array[row, col] = 0
            
# print(empty_array) 
# print(empty_array[row, -1])

        
        

    

# grayscale_image = convert_to_grayscale(image)
# resized_image = resize_image(grayscale_image, width=200, height=200)
# brightness_array = convert_to_numpy_array(resized_image)  # values 0–255

# # 3. Define Spiral Path Parameters
# r_max = image_radius_in_pixels
# r = 0
# theta = 0
# theta_step = small_angle_increment
# r_step_per_theta = (r_max - r_min) / (2 * math.pi * num_spirals)  # spiral density

# # 4. Initialize Output List
# commands = []

# # 5. Generate Spiral Path
# while r < r_max:
#     # Convert polar to Cartesian
#     x = center_x + r * cos(theta)
#     y = center_y + r * sin(theta)

#     # Check bounds
#     if x in image bounds and y in image bounds:
#         brightness = sample_pixel(brightness_array, x, y)  # 0=black, 255=white

#         # Decide action based on brightness
#         if brightness < dark_threshold:
#             commands.append(f"DRAW {x} {y}")
#         else:
#             commands.append(f"MOVE {x} {y}")

#     # Update spiral position
#     theta += theta_step
#     r += r_step_per_theta

# # 6. Output Commands
# save_commands_to_file(commands, "spiral_path.txt")

# # Optional: stream over serial
# # for cmd in commands:
# #     serial_port.write(cmd + '\n')
