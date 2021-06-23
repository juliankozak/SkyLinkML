from utils.model_maskrcnn_resnet50_FastRCNNPredictor import *
from PIL import Image
from utils.mask_visualization import *
import datetime
import time

model_state = "train/models/mod_2/model_state_dict.pt"
dir_images = "images/best_of_flight_1_and_2"
#dir_images = 'train/training_data/recording_flight_1/mentalist_in_the_image/best_of_flight_1_and_2'

model, device = get_model_FasterRCNN_mobilnet_backbone()
load_state(model, model_state)
dataset, _ = create_dataset_and_dataloader(dir_images)
print("Model and dataset ready")


with torch.no_grad():

    for i in range(dataset.__len__()):
    #for i in range(1):
        print("i = ", i, " - starttime", str(datetime.datetime.now()))
        t_start = time.time()
        image_pillow, _ = dataset.__getitem__(i)
        t_image_loaded = time.time()
        #res = run_model(model, image_pillow, device)
        image_device = image_pillow.to(device)
        t_image_on_gpu = time.time()
        prediction = model([image_device])
        t_model_calculated = time.time()

        print(" load image: {} to device: {} model: {}".format(t_image_loaded-t_start, t_image_on_gpu-t_image_loaded, t_model_calculated-t_image_on_gpu))
        #mask = res[0]['masks'][0, 0].mul(255).byte().cpu().numpy()
        #image = image_pillow.mul(255).squeeze().permute(1,2,0).byte().cpu().numpy()  # dim = (h, w, 3)

        #create_figure_image_and_mask(image, mask)
