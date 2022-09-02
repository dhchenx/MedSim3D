
from PIL import Image

body_part_root=f"../datasets/Male/abdomen"
file_name='a_vm1455.png'
image_path=body_part_root+"/"+file_name

target_color=[37,86,115]

image = Image.open(image_path)
# image.show()
image_data = image.load()
height,width = image.size
for loop1 in range(height):
    for loop2 in range(width):
        r,g,b = image_data[loop1,loop2]
        if r==target_color[0] and g==target_color[1] and b==target_color[2]:
            image_data[loop1,loop2] = 0,0,0

image.save(file_name)


