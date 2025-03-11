import os
from PIL import Image

def image_to_hex_list(image_path):
    img = Image.open(image_path).convert("RGBA")  
    pixels = list(img.getdata())  
    hex_list = [str(img.size[0]), str(img.size[1])]

    for r, g, b, a in pixels:
        if a == 0: 
            hex_list.append(str(0))
        else:
            hex_list.append(str((r << 16) | (g << 8) | b))

    return hex_list

def process_images_in_folder(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".png"): 
            file_in = os.path.join(folder, filename)
            file_out = os.path.join(folder, f"{os.path.splitext(filename)[0]}.raw")
            
            data = image_to_hex_list(file_in)
            with open(file_out, "w") as file:
                file.write(";".join(data))
            
            print(f"Converted: {filename} -> {os.path.basename(file_out)}")

folder_path = "Assets/Textures/Fonts/Background/"
process_images_in_folder(folder_path)