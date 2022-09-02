from PIL import Image

im = Image.open("a_vm1455.png")
width, height = im.size
im = im.resize((int(width/2),int(height/2)))

im1=im.load()
pix_color=im1[int(221/2),int(518/2)]

print(pix_color)