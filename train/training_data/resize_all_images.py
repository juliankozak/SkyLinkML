from utils.image_editing import *
from utils.os import *
import numpy as np


dir_images = "training_data/images_original"
dir_masks = "training_data/masks_original"
new_size = 400

dir_images_new = "training_data/images_resized_{}px".format(new_size)
dir_masks_new = "training_data/masks_resized_{}px".format(new_size)

mkdir(dir_images_new)
mkdir(dir_masks_new)

print("New size: {}".format(new_size))
print("Downsizing all images of {}".format(dir_images))
# for image in os.listdir(dir_images):
#     print(image)
#     if image.startswith("."):
#         continue
#     im = cv2.imread(os.path.join(dir_images, image))
#     im_new = image_downsize(im, new_size)
#     cv2.imwrite(os.path.join(dir_images_new, image), im_new)


print("Downsizing all masks {}".format(dir_masks))
for mask in os.listdir(dir_masks):
    print(mask)
    if(mask.startswith(".")):
        continue
    ma = cv2.imread(os.path.join(dir_masks, mask), cv2.IMREAD_GRAYSCALE)
    ma_new = image_downsize(ma, new_size, cv2.INTER_NEAREST) # use INTER_NEAREST to keep values {0, 255} and avoid averaging at the borders
    cv2.imwrite(os.path.join(dir_masks_new, mask), ma_new)
print("Finish.")
