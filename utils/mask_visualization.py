import numpy as np
import matplotlib.pyplot as plt


def create_figure_image_and_mask(image_np_3ch, mask_np_1ch):
    # image: 3 channel
    # mask: 1 channel, greyscale
    fig = plt.figure(figsize=(19, 9))
    rows = 3
    columns = 4

    ### 1
    fig.add_subplot(rows, columns, 1)
    plt.imshow(image_np_3ch)
    plt.axis("off")
    plt.title("Original image ({} x {} px)".format(image_np_3ch.shape[0], image_np_3ch.shape[1]))

    ### 2
    fig.add_subplot(rows, columns, 2)
    plt.imshow(mask_np_1ch, cmap='gray', vmin=0, vmax=255)
    plt.axis("off")
    plt.title("Mask (greyscale)")

    ### 3
    fig.add_subplot(rows, columns, 3)
    # overlay bild mit maske
    #  dort wo die maske -> durch rot ersetzen -> [255, 0, 0]
    #  dort wo keine maske -> originales bild lassen

    # choose threshold somewhere between 1 and 255
    threshold = 150
    mask = (mask_np_1ch > threshold) * 1    # 2d array, value = 1 -> mask, value = 0 -> background

    overlay_color = np.uint8([255, 0, 255])

    image_masked = np.array(image_np_3ch) # make copy
    image_masked[:, :, 0] = (mask == 0) * image_masked[:, :, 0]
    ch_r = np.ndarray(mask.shape, dtype=np.uint8)
    ch_r = (mask == 1) * overlay_color[0]
    image_masked[:, :, 0] += ch_r

    image_masked[:, :, 1] = (mask == 0) * image_masked[:, :, 1]
    ch_g = np.ndarray(mask.shape, dtype=np.uint8)
    ch_g = (mask == 1) * overlay_color[1]
    image_masked[:, :, 1] += ch_g

    image_masked[:, :, 2] = (mask == 0) * image_masked[:, :, 2]
    ch_b = np.ndarray(mask.shape, dtype=np.uint8)
    ch_b = (mask == 1) * overlay_color[2]
    image_masked[:, :, 2] += ch_b

    plt.imshow(image_masked)
    plt.axis("off")
    plt.title("fixed threshold = {}".format(threshold))

    ### 5
    fig.add_subplot(rows, columns, 5)
    pos = np.asarray(mask_np_1ch > 0).nonzero() #np.where(mask_np_1ch > 0)
    xmin = np.min(pos[1])
    xmax = np.max(pos[1])
    ymin = np.min(pos[0])
    ymax = np.max(pos[0])
    im_3ch_zoom = image_np_3ch[ymin:ymax, xmin:xmax, :]
    plt.imshow(im_3ch_zoom)
    plt.axis("off")
    plt.title("Original image - zoom")

    ### 6
    fig.add_subplot(rows, columns, 6)
    plt.imshow(mask_np_1ch[ymin:ymax, xmin:xmax], cmap='gray', vmin=0, vmax=255)
    plt.axis("off")
    plt.title("Mask (greyscale) - zoom")

    ### 7
    fig.add_subplot(rows, columns, 7)
    plt.imshow(image_masked[ymin:ymax, xmin:xmax, :])
    plt.axis("off")
    plt.title("fixed threshold = {} - zoom".format(threshold))

    ### 10
    fig.add_subplot(rows, columns, 10)
    vals = np.ravel(mask_np_1ch)
    vals2 = vals[vals != 0] # list all greyscale values between 1 and 255, exclude 0 since it corresponds background
    plt.hist(vals2, bins=25)
    plt.xlabel("greyscale value")
    plt.ylabel("number of occurences")
    plt.title("values mask (greyscale)")


    ### 8
    fig.add_subplot(rows, columns, 8)
    percentile = 50
    threshold_p = np.percentile(vals2, percentile)

    mask_p = (mask_np_1ch > threshold_p) * 1
    image_masked_p = np.array(image_np_3ch)  # make copy
    image_masked_p[:, :, 0] = (mask_p == 0) * image_masked_p[:, :, 0]
    ch_r = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_r = (mask_p == 1) * overlay_color[0]
    image_masked_p[:, :, 0] += ch_r

    image_masked_p[:, :, 1] = (mask_p == 0) * image_masked_p[:, :, 1]
    ch_g = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_g = (mask_p == 1) * overlay_color[1]
    image_masked_p[:, :, 1] += ch_g

    image_masked_p[:, :, 2] = (mask_p == 0) * image_masked_p[:, :, 2]
    ch_b = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_b = (mask_p == 1) * overlay_color[2]
    image_masked_p[:, :, 2] += ch_b

    plt.imshow(image_masked_p[ymin:ymax, xmin:xmax, :])
    plt.axis("off")
    plt.title("percentile = {}, threshold = {} - zoom".format(percentile, threshold_p))

    ### 12
    fig.add_subplot(rows, columns, 12)
    percentile = 70
    threshold_p = np.percentile(vals2, percentile)

    mask_p = (mask_np_1ch > threshold_p) * 1
    image_masked_p = np.array(image_np_3ch)  # make copy
    image_masked_p[:, :, 0] = (mask_p == 0) * image_masked_p[:, :, 0]
    ch_r = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_r = (mask_p == 1) * overlay_color[0]
    image_masked_p[:, :, 0] += ch_r

    image_masked_p[:, :, 1] = (mask_p == 0) * image_masked_p[:, :, 1]
    ch_g = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_g = (mask_p == 1) * overlay_color[1]
    image_masked_p[:, :, 1] += ch_g

    image_masked_p[:, :, 2] = (mask_p == 0) * image_masked_p[:, :, 2]
    ch_b = np.ndarray(mask_p.shape, dtype=np.uint8)
    ch_b = (mask_p == 1) * overlay_color[2]
    image_masked_p[:, :, 2] += ch_b

    plt.imshow(image_masked_p[ymin:ymax, xmin:xmax, :])
    plt.axis("off")
    plt.title("percentile = {}, threshold = {} - zoom".format(percentile, threshold_p))

    plt.show()

