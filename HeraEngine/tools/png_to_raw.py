from PIL import Image

file = "Assets/Textures/Menus/Main/title"


def image_to_hex_list(image_path):
    img = Image.open(image_path).convert("RGBA")  
    pixels = list(img.getdata())  
    hex_list = [str(img.size[0]),str(img.size[1])]

    for r, g, b, a in pixels:
        if a == 0: 
            hex_list.append(str(0))
        else:
            hex_list.append(str((r << 16) | (g << 8) | b))

    return hex_list

file_in = f"{file}.png"
file_out = f"{file}.raw"

data = image_to_hex_list(file_in)
with open(file_out,"w") as file:
    file.write(str(";".join(data)))
