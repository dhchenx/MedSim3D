import cv2

baseline_image_path="datasets/a_vm1455_baseline.png"

baseline_image = cv2.imread(baseline_image_path)
height,width,dim=baseline_image.shape
print(baseline_image.shape)
image=cv2.cvtColor(baseline_image,cv2.COLOR_BGR2GRAY)
image=cv2.resize(image,dsize=(int(width/2),int(height/2)))

cv2.imshow("baseline gray",image)

t=50
edges = cv2.Canny(image, t, 3 * t)

cv2.imshow("canny",edges)

cv2.waitKey()