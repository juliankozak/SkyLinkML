from utils.model_maskrcnn_resnet50_FastRCNNPredictor import *
from PIL import Image
from utils.mask_visualization import *

model_state = "train/models/mod_2/model_state_dict.pt"
#dir_images = "train/training_data/recording_flight_1/mentalist_in_the_image/best_of_flight_1_and_2"
dir_images = "train/training_data/recording_flight_2/best_of"

model, device = get_model_FasterRCNN_mobilnet_backbone()
load_state(model, model_state)
dataset, dataloader = create_dataset_and_dataloader(dir_images)
print("Model and dataset ready")


for i in range(dataset.__len__()):
#for i in range(1):
    print("i = ", i)
    image_pillow, _ = dataset.__getitem__(i)
    res = run_model(model, image_pillow, device)

    mask = res[0]['masks'][0, 0].mul(255).byte().cpu().numpy()
    image = image_pillow.mul(255).squeeze().permute(1,2,0).byte().cpu().numpy()  # dim = (h, w, 3)

    create_figure_image_and_mask(image, mask)
