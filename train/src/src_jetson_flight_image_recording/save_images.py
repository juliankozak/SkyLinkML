import cv2
import datetime
import os
import errno
import argparse
import time

# Defaults to 1280x720 @ 60fps
# display_width and display_height determine the size of the window on the screen

CAPTURE_WIDTH = 1348     # 1280
CAPTURE_HEIGHT = 762    # 720
DISPLAY_WIDTH = 1348
DISPLAY_HEIGHT = 762
FRAMERATE = 30
FLIP_MEHTOD = 0  # To flip the image, modify the flip_method parameter (0 and 2 are the most common)

parser = argparse.ArgumentParser(description='Set recording parameters')
parser.add_argument('--delta', type=int, help='time between two images in seconds')
parser.add_argument('--recording_time', type=int, help='duration of the recording in seconds')
parser.add_argument('--time_before_recording', type=int, help='seconds before recording starts')
parser.add_argument('--title', type=str, help='titel of directory')




def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def gstreamer_pipeline(
    capture_width=720, 
    capture_height=680, 
    display_width=720,
    display_height=680,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def save_images(delta_t=1, recording_duration_s=60, foldername="demo"):
    
    global CAPTURE_WIDTH
    global CAPTURE_HEIGHT
    global DISPLAY_WIDTH 
    global DISPLAY_HEIGHT 
    global FRAMERATE 
    global FLIP_MEHTOD
    
    in_pipeline =  gstreamer_pipeline(capture_width=CAPTURE_WIDTH, capture_height=CAPTURE_HEIGHT, display_width=DISPLAY_WIDTH,
    display_height=DISPLAY_HEIGHT,framerate=FRAMERATE,flip_method=FLIP_MEHTOD)
    
    cap = cv2.VideoCapture(in_pipeline, cv2.CAP_GSTREAMER)

    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%dT%H%M%S")
    print(dt_string)

    if cap.isOpened():
        
        red_counter = 0
        red_factor = FRAMERATE*delta_t
        image_counter = 0
        
        num_images = int(recording_duration_s / delta_t)

        directory = "./images/" + dt_string + "/" + foldername
        mkdir(directory)

        print("reduction factor: {}".format(recording_duration_s))
        print("")

        while image_counter < num_images:
            ret_val, img = cap.read()
            if red_counter < red_factor:
                red_counter += 1
                continue

            image_time = datetime.datetime.now()
            image_time_string = image_time.strftime("%Y-%m-%d  %H:%M:%S")
            print("saving image {}".format(image_time_string))
            filename = "image_{}.png".format(image_counter)
            cv2.imwrite(os.path.join(directory,filename), img)
            
            image_counter += 1
            red_counter = 0 # reset reduction counter

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    args = parser.parse_args()
    print("argparse:")
    print("delta = {} s".format(args.delta))
    print("recording time = {}".format(args.recording_time))
    print("time_before_recording = {}".format(args.time_before_recording))
    print("sleep...")
    time.sleep(args.time_before_recording)
    print("Starting recording.")
    save_images(delta_t=args.delta, recording_duration_s=args.recording_time, foldername=args.title)
