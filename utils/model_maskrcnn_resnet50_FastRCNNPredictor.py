import os
import torch
import torch.utils.data
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection import FasterRCNN

from PIL import Image
import numpy as np

import train.src.pytorch_utils.utils as utils
import train.src.pytorch_utils.transforms as T
from utils.os import listdir_nohidden


def get_model():
    num_classes = 2
    # load an instance segmentation model pre-trained on COCO
    print("Loading Mask R-CNN model based on Resnet50")
    model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)

    # get the number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    # replace the pre-trained head with a new one
    print("Replace head with Fast R-CNN Predictor, 2 classes")
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # now get the number of input features for the mask classifier
    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    # and replace the mask predictor with a new one
    model.roi_heads.mask_predictor = MaskRCNNPredictor(in_features_mask,
                                                       hidden_layer,
                                                       num_classes)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Device: ", device)
    model.to(device)
    return model, device


def get_model_FasterRCNN_mobilnet_backbone():
    # load a pre-trained model for classification and return
    # only the features
    backbone = torchvision.models.mobilenet_v2(pretrained=True).features
    # FasterRCNN needs to know the number of
    # output channels in a backbone. For mobilenet_v2, it's 1280
    backbone.out_channels = 1280

    # let's make the RPN generate 5 x 3 anchors per spatial
    # location, with 5 different sizes and 3 different aspect
    # ratios. We have a Tuple[Tuple[int]] because each feature
    # map could potentially have different sizes and
    # aspect ratios
    anchor_generator = AnchorGenerator(sizes=((32, 64, 128, 256, 512),),
                                       aspect_ratios=((0.5, 1.0, 2.0),))

    # let's define what are the feature maps that we will
    # use to perform the region of interest cropping, as well as
    # the size of the crop after rescaling.
    # if your backbone returns a Tensor, featmap_names is expected to
    # be [0]. More generally, the backbone should return an
    # OrderedDict[Tensor], and in featmap_names you can choose which
    # feature maps to use.
    roi_pooler = torchvision.ops.MultiScaleRoIAlign(featmap_names=['0'],
                                                    output_size=7,
                                                    sampling_ratio=2)
    # bugfix: https://discuss.pytorch.org/t/error-torchvision-object-detection-finetuning-tutorial/86766

    # put the pieces together inside a FasterRCNN model
    model = FasterRCNN(backbone,
                       num_classes=2,
                       rpn_anchor_generator=anchor_generator,
                       box_roi_pool=roi_pooler)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Device: ", device)
    model.to(device)
    return model, device


def load_state(model, file_state_dictionary):
    print("Loading state dictionary from ", file_state_dictionary)
    if torch.cuda.is_available():
        maplocation = lambda storage, loc: storage.cuda(0)
    else:
        maplocation = torch.device('cpu')
    print("map location: ", maplocation)
    model.load_state_dict(torch.load(file_state_dictionary, map_location=maplocation))
    model.eval()
    print('State dictionary loaded.')
    print('Model in evaluation mode.')


def get_transform(train=False):
    transforms = [T.ToTensor()]
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)


def create_dataset_and_dataloader(directory_images, batchsize=1, numworker=1, directory_masks=None, train=False, n_test_images=50):
    print("Creating dataset and dataloader")
    print("Image directory: ", directory_images)
    if train:
        print("Mask directory: ", directory_masks)
    print("batchsize: ", batchsize)
    print("numworker: ", numworker)
    if train:
        print("num test images: ", n_test_images)

    print("{}".format("Train mode" if train else "Evaluation mode"))

    if not train:
        dataset = ImageDataset(directory_images, get_transform())
        print("{} images in dataset".format(dataset.__len__()))
        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=batchsize, shuffle=False, num_workers=numworker,
            collate_fn=utils.collate_fn)
        return dataset, data_loader

    else:   # train=True
        torch.manual_seed(1)

        dataset = ImageDataset(directory_images, directory_masks=directory_masks, transforms=get_transform(train=True), train=True)
        indices = torch.randperm(len(dataset)).tolist()
        dataset = torch.utils.data.Subset(dataset, indices[:-n_test_images])

        dataset_test = ImageDataset(directory_images, directory_masks=directory_masks, transforms=get_transform(train=False), train=True)
        dataset_test = torch.utils.data.Subset(dataset_test, indices[-n_test_images:])

        data_loader = torch.utils.data.DataLoader(dataset, batch_size=batchsize, shuffle=True, num_workers=numworker, collate_fn=utils.collate_fn)

        data_loader_test = torch.utils.data.DataLoader(dataset_test, batch_size=batchsize, shuffle=False, num_workers=numworker, collate_fn=utils.collate_fn)

        return dataset, data_loader, dataset_test, data_loader_test


def run_model(model, image, device):
    with torch.no_grad():
        image_device = image.to(device)
        prediction = model([image_device])
    return prediction


class ImageDataset(torch.utils.data.Dataset):
    """
    naming of training images and masks:
    img_000.png
    mask_000.png
    images and masks need be stored in different directories (dir_images and dir_masks)
    """
    def __init__(self, directory_images, transforms=None, directory_masks=None, train=False):
        self.dir_images = directory_images
        self.transforms = transforms
        self.imgs = listdir_nohidden(self.dir_images)
        self.train = train
        if self.train:
            self.dir_masks = directory_masks
            self.masks = listdir_nohidden(self.dir_masks)   # sorted according to the number since the prefix is same

    def __getitem__(self, idx):
        # load images ad masks
        img_path = os.path.join(self.dir_images, self.imgs[idx])
        img = Image.open(img_path).convert("RGB")

        if not self.train:
            if self.transforms is not None:
                img, _ = self.transforms(img, None)
                target = None;

        else:   # Train = true -> load masks from disk
            mask_path = os.path.join(self.dir_masks, self.masks[idx])
            mask = Image.open(mask_path)    # mask not converted to RGB
            mask = np.array(mask)
            obj_ids = np.unique(mask)   # instances are encoded as different colors
            obj_ids = obj_ids[1:]       # first id is the background, so remove it

            masks = (mask == obj_ids[:, None, None])    # split the color-encoded mask into a set of binary masks

            # get bounding box coordinates for each mask
            num_objs = len(obj_ids)
            boxes = []
            for i in range(num_objs):
                pos = np.where(masks[i])
                xmin = np.min(pos[1])
                xmax = np.max(pos[1])
                ymin = np.min(pos[0])
                ymax = np.max(pos[0])
                boxes.append([xmin, ymin, xmax, ymax])

            boxes = torch.as_tensor(boxes, dtype=torch.float32)

            labels = torch.ones((num_objs,), dtype=torch.int64)     # there is only one class
            masks = torch.as_tensor(masks, dtype=torch.uint8)
            image_id = torch.tensor([idx])
            area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
            iscrowd = torch.zeros((num_objs,), dtype=torch.int64)   # suppose all instances are not crowd

            target = {
                "boxes": boxes,
                "labels": labels,
                "masks": masks,
                "image_id": image_id,
                "area": area,
                "iscrowd": iscrowd }

            if self.transforms is not None:
                img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)

