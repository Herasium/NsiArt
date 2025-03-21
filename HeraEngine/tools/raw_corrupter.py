import os
import time
import random
import numpy as np
from tqdm import tqdm
from PIL import Image

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_table(results):
    header = ("Input File", "Output File", "Status")
    all_rows = [header] + results
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(3)]
    
    def print_border():
        print("+" + "+".join("-" * (w + 2) for w in col_widths) + "+")
    
    print_border()
    print("| " + " | ".join(header[i].ljust(col_widths[i]) for i in range(3)) + " |")
    print_border()
    for row in results:
        print("| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(3)) + " |")
    print_border()

def image_to_hex_list(image_path):
    img = Image.open(image_path).convert("RGBA")
    pixels = list(img.getdata())
    hex_list = [str(img.size[0]), str(img.size[1])]
    
    for r, g, b, a in pixels:
        if a == 0:
            hex_list.append("0")
        else:
            hex_list.append(str((r << 16) | (g << 8) | b))
    
    return hex_list

def corrupt_raw_data(raw_list):

    width = int(raw_list[0])
    height = int(raw_list[1])
    
    pixel_data = np.array(raw_list[2:], dtype=np.uint32).reshape((int(height), int(width)))
    

    n_cols = pixel_data.shape[1]
    indices = np.arange(n_cols)
    shift_range = 15
    random_shifts = np.random.randint(-shift_range, shift_range + 1, size=n_cols)
    new_order = np.argsort(indices + random_shifts)
    pixel_data = pixel_data[:, new_order]
    
    random_factors = np.random.randint(0, 256, size=(pixel_data.shape[0], pixel_data.shape[1]), dtype=np.uint32)
    corrupted_array = pixel_data * random_factors
    
    corrupted_pixels = corrupted_array.flatten().astype(str).tolist()
    
    corrupted_raw_list = [str(width), str(height)] + corrupted_pixels
    return ";".join(corrupted_raw_list)

def process_images_recursively(root_folder):
    conversion_results = []

    files_to_process = []
    for subdir, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.lower().endswith(".png"):
                file_in = os.path.join(subdir, filename)
                file_out = os.path.join(subdir, f"{os.path.splitext(filename)[0]}.raw")
                files_to_process.append((file_in, file_out))
    

    for file_in, file_out in tqdm(files_to_process):
        conversion_results.append((file_in, file_out, "Processing"))

        
        data = image_to_hex_list(file_in)
        with open(file_out, "w") as file:
            file.write(";".join(data))
        
        corrupted_data = corrupt_raw_data(data)
        corrupted_file_out = f"{file_out}.corrupted"
        with open(corrupted_file_out, "w") as file:
            file.write(corrupted_data)

        conversion_results[-1] = (file_in, f"{file_out} & {corrupted_file_out}", "Converted & Corrupted")

    
    print("\nAll files processed.")

folder_path = "Assets/Textures/"
process_images_recursively(folder_path)
