'''
Create masks from annotated images.

masks were drawn manually on ipad with a red pen
some images were deleted on ipad

1) rename and copy all images that have masks to images_cleaned directory
2) create masks from images with red annotation
'''
import sys

from PIL import Image
from shutil import copyfile
from os.path import join as join
from utils.os import *
import cv2



flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
# print(flags)

dir_images_raw = 'data/uncleaned'
dir_masks_raw = 'data/masks_ipad'

dir_images_cleaned = 'data/images_cleaned'
dir_masks_cleaned = 'data/masks_cleaned'

filenames_orig = os.listdir(dir_masks_raw)
print(filenames_orig)

mkdir(dir_images_cleaned)
mkdir(dir_masks_cleaned)

basename_image = 'img_'
basename_mask = 'mask_'

counter = 0
for file in filenames_orig:
    print("current image: ", join(dir_images_raw, file))
    copyfile(join(dir_images_raw, file), join(dir_images_cleaned, basename_image+str(counter)+'.png'))

    try:
        m = cv2.imread(join(dir_masks_raw, file))
        m = cv2.cvtColor(m, cv2.COLOR_BGR2RGB)

        red_l1 = (252, 13, 27) #ipad red
        red_l2 = (252, 13, 27) #ipad red

        mask = cv2.inRange(m, red_l1, red_l2)
        cv2.imwrite(join(dir_masks_cleaned, basename_mask+str(counter)+'.png'), mask)

    except:
        print("SKIPPED image", sys.exc_info()[0])

    counter += 1



