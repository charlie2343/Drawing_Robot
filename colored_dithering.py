
from PIL import Image     # Pillow for image processing
import numpy as np   # NumPy for fast matrix math
import math    # For trig functions
import serial  # Optional: to send via serial

# 2. Load and Preprocess Image
img = Image.open("dragon.png")
new_width = 800
new_height = int(img.height * (new_width / img.width))  # Maintain aspect ratio
print(f"Original size: {img.size}, New size: {new_width}x{new_height}")
img = img.resize((new_width, new_height))
#img = img.convert("L")  # Convert to grayscale
img.show()

pixel_array = np.array(img, dtype=float)  # Convert to NumPy array
print(f"Pixel array shape: {pixel_array.shape}")
print(pixel_array)


for row in range(0,pixel_array.shape[0]): 
    for col in range(0,pixel_array.shape[1]):
        pixel_value = pixel_array[row, col]
        #print(f"Pixel value: {pixel_value}, Type: {type(pixel_value)}")
        for data in range(0,len(pixel_value)): 
            error = 0
            max_dist = 255 - pixel_value[data]
            if max_dist > pixel_value[data]: 
                #drawstipple() # do i just change the pixel value or shoudl I draw a circle? 
                error = pixel_value[data]
                pixel_array[row, col,data] = 0 
            else: 
                error = pixel_value[data] -255
                pixel_array[row, col,data] = 255
            try:
                if col != 0:
                    pixel_array[row+1, col-1, data] += error * 3/16 
                pixel_array[row, col+1, data] += error * 7/16
                pixel_array[row+1, col, data] += error * 5/16
                pixel_array[row+1, col+1, data] += error * 1/16
            except IndexError:
                pass
        
#print(pixel_array)
# distribute error
# check if pixel is not at col[0] or row pixel_array.shape[0] -1: 
# final_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
# final_image = Image.fromarray(final_array)
# final_image.show()
# final_image.save("tiger_dithered.jpg")

def limited_pallete(factor): 
    for row in range(0,pixel_array.shape[0]): 
        for col in range(0,pixel_array.shape[1]):
            for data in range(0,len(pixel_value)):
                pixel_value[data] = round(factor * pixel_value[data]/255) * (255/factor)
    limited_array = np.clip(pixel_array, 0, 255).astype(np.uint8)
    limited_image = Image.fromarray(limited_array)
    limited_image.show()
    limited_image.save("reduced_image.jpg")
limited_pallete(1) 
    
def create_combined(): 
    total_width = img.width + final_image.width
    combined = Image.new("RGB", (total_width, img.height))

    # Paste images side by side
    combined.paste(img, (0, 0))
    combined.paste(final_image, (img.width, 0))

    # Show or save
    combined.show()
    combined.save("combined.jpg")