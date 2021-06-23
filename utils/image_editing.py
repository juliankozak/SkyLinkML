import cv2


def image_downsize(image, max_size=300, inter=cv2.INTER_LINEAR):
    """
        Downsize an image keeping the aspect ratio:
        the large dimension of the image will be set to max_size
        and the other dimension calculate in order to maintain the aspect ratio
        if the image is smaller than max_size, input image will be returned
        interpolation:
        default: cv2.INTER_LINEAR
        use cv2.INTER_NEAREST for masks {0, 255} -> will otherwise be averaged at border of mask and
                                                                        all values in the range [0,255] will be contained!
    """
    dim = None
    (h, w) = image.shape[:2]
    ratio = float(h) / float(w)   # ratio = h / w

    if h <= max_size and w <= max_size:
        return image

    if w > h:
        w_new = max_size
        h_new = int(w_new * ratio)
        dim = (w_new, h_new)
    else:
        h_new = max_size
        w_new = int(float(h_new) / float(ratio))
        dim = (w_new, h_new)

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
