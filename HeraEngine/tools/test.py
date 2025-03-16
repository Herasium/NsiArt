from PIL import Image
import numpy as np
from collections import Counter

def most_common_color(tile):
    """Return the most common color in a 4x4 tile."""
    pixels = list(tile.getdata())
    return Counter(pixels).most_common(1)[0][0]

def image_to_color_matrix(image_path):
    """Divides the image into 4x4 tiles and returns a matrix of the most common color of each tile."""
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # Ensure dimensions are multiples of 4
    width -= width % 4
    height -= height % 4
    img = img.crop((0, 0, width, height))
    
    matrix = []
    for y in range(0, height, 4):
        row = []
        for x in range(0, width, 4):
            tile = img.crop((x, y, x+4, y+4))
            row.append(most_common_color(tile))
        matrix.append(row)
    
    return np.array(matrix)

def matrix_to_bw_image(matrix):
    """
    Creates a new image with one pixel per matrix element.
    If the matrix element (the most common color) is (0, 0, 0) then the pixel is black; otherwise, white.
    """
    rows, cols = matrix.shape[0], matrix.shape[1]
    new_img = Image.new("RGB", (cols, rows))
    pixels = new_img.load()
    
    for i in range(rows):
        for j in range(cols):
            # Use np.array_equal to compare the array with (0, 0, 0)
            if np.array_equal(matrix[i][j], (0, 0, 0)):
                pixels[j, i] = (0, 0, 0)
            else:
                pixels[j, i] = (255, 255, 255)
    return new_img


# Example usage:
image_path = "HeraEngine/tools/map.png"  # Replace with the path to your image file
color_matrix = image_to_color_matrix(image_path)
bw_image = matrix_to_bw_image(color_matrix)
bw_image.save("collision_map.png")       # Display the resulting image
# bw_image.save("output.png")  # Optionally, save the image to a file
