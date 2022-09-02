import cv2
import numpy as np
import matplotlib.pyplot as plt
import quickcsv
from skimage import morphology
import numpy as np
import skimage
from skimage.metrics import structural_similarity
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import logging

logger = logging.getLogger('my-logger')
logger.propagate = False
def remove_noise1(image_path,intensity=5,rect1=5,rect2=2):
    img = cv2.imread(image_path)

    # cv2.imshow('Original', img)

    img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > intensity).astype('uint8')

    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect1, rect1))
    se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect2, rect2))
    mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

    mask = np.dstack([mask, mask, mask]) / 255
    out = img * mask

    # cv2.imshow('Output', out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite('output1.png', out)

def remove_noise2(image_path,min_size=2,connectivity=2,thresold=0.1):
    # read the image, grayscale it, binarize it, then remove small pixel clusters
    im1 = plt.imread(image_path)
    im = skimage.color.gray2rgb(im1)
    grayscale = skimage.color.rgb2gray(im)

    binarized = np.where(grayscale > thresold, 1, 0)
    processed = morphology.remove_small_objects(binarized.astype(bool), min_size=min_size, connectivity=connectivity).astype(int)

    # black out pixels
    mask_x, mask_y = np.where(processed == 0)
    im[mask_x, mask_y, :3] = 0

    # plot the result
    # plt.figure(figsize=(10, 10))
    # plt.imshow(im)

    plt.imsave("output2.png", im)

def evaluate1(image_path):
    list_result=[]
    print("Rect1\tRect2\tSSIM score\tDVSImMscore")
    for rect1 in range(1, 10+1):
        for rect2 in range(1,10+1):
            remove_noise1(image_path=image_path, rect1=rect1,rect2=rect2)
            score_ssim = ssim('datasets/baseline_edges.png', 'output1.png')
            score_dvsim = dvsim('datasets/baseline_edges.png', 'output1.png')
            print(f"{rect1}\t{rect2}\t{score_ssim}\t{score_dvsim}")
            list_result.append({
                "rect1":rect1,
                "rect2":rect2,
                "ssim":score_ssim,
                "dvsim":score_dvsim
            })
    quickcsv.write_csv("eval1.csv",list_result)

def evaluate2(image_path):
    list_result=[]
    print("Min Size\tConnectivity\tSSIM score\tDVSImMscore")
    for m in range(1, 10+1):
        for c in range(1,10+1):
            remove_noise2(image_path=image_path,min_size=m,connectivity=c)
            score_ssim = ssim('datasets/baseline_edges.png', 'output2.png')
            score_dvsim = dvsim('datasets/baseline_edges.png', 'output2.png')
            print(f"{m}\t{c}\t{score_ssim}\t{score_dvsim}")
            list_result.append({
                "Min Size":m,
                "Connectivity":c,
                "SSIM":score_ssim,
                "DVSIM":score_dvsim
            })
    quickcsv.write_csv("eval2.csv", list_result)

def evaluate2_connectivity(image_path):
    print("Connectivity\tSSIM score\tDVSIm score")
    for c in range(1,10):
        remove_noise2(image_path=image_path, connectivity=c)
        score_ssim=ssim('datasets/baseline_edges.png','output2.png')
        score_dvsim=dvsim('datasets/baseline_edges.png','output2.png')
        print(f"{c}\t{score_ssim}\t{score_dvsim}")

def ssim(image1,image2):
    baseline = cv2.imread(image1)
    baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
    second = cv2.imread(image2)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)
    score2, diff2 = structural_similarity(baseline_gray, second_gray, full=True)
    return score2

def dvsim(image1,image2):
    # Load the OpenAI CLIP Model

    # Next we compute the embeddings
    # To encode an image, you can use the following code:
    # from PIL import Image
    # encoded_image = model.encode(Image.open(filepath))
    image_names = [image1,image2]
   #  print(image_names)
    # print("Images:", len(image_names))
    encoded_image = model.encode([Image.open(filepath) for filepath in image_names], batch_size=128,
                                 convert_to_tensor=True, show_progress_bar=True)

    # Now we run the clustering algorithm. This function compares images aganist
    # all other images and returns a list with the pairs that have the highest
    # cosine similarity score
    processed_images = util.paraphrase_mining_embeddings(encoded_image)
    NUM_SIMILAR_IMAGES = 10

    # =================
    # DUPLICATES
    # =================
    # print('Finding duplicate images...')
    # Filter list for duplicates. Results are triplets (score, image_id1, image_id2) and is scorted in decreasing order
    # A duplicate image will have a score of 1.00
    # It may be 0.9999 due to lossy image compression (.jpg)
    # duplicates = [image for image in processed_images if image[0] >= 0.9999999]
    duplicates = processed_images
    # print(duplicates)
    # Output the top X duplicate images
    for score, image_id1, image_id2 in duplicates[0:NUM_SIMILAR_IMAGES]:
        # print("\nScore: {:.3f}%".format(score * 100))
        # print(image_names[image_id1])
        # print(image_names[image_id2])
        return score

print('Loading CLIP Model...')
model = SentenceTransformer('clip-ViT-B-32')

# https://stackoverflow.com/questions/11541154/checking-images-for-similarity-with-opencv
if __name__=="__main__":
    root_path = "datasets/evaluate1"

    image_path = root_path + "/" + "iso2_a_vm1455.png"
    # evaluate1(image_path=image_path)
    evaluate2(image_path=image_path)
    # evaluate2_connectivity(image_path=image_path)


'''


if __name__=="__main__":
    root_path = "datasets/evaluate1"

    image_path = root_path + "/" + "iso2_a_vm1455.png"
    remove_noise1(image_path=image_path)
    remove_noise2(image_path=image_path)

    # Method #1: Structural Similarity Index (SSIM)
    # Compute SSIM between two images
   
    baseline=cv2.imread("datasets/baseline_edges.png")
    first = cv2.imread('output1.png')
    second = cv2.imread('output2.png')
    # Convert images to grayscale
    baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
    first_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    second_gray = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)
    score1, diff1 = structural_similarity(baseline_gray, first_gray, full=True)
    print("Similarity Score1: {:.3f}%".format(score1 * 100))
    score2, diff2 = structural_similarity(baseline_gray, second_gray, full=True)
    print("Similarity Score2: {:.3f}%".format(score2 * 100))

    # 2 Method #2: Dense Vector Representations

'''


