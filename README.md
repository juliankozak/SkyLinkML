# RC tug plane localization (detection and autopilot)
Goal: Using a computer vision AI-based model, the glider localizes the tug aircraft in real time and stays automatically on the optimal flight path behind the tug aircraft until reaching the desired altitude. Glider pilot disables the automatic mode before disconnecting from the tug aircraft, the tug aircraft prepares for landing and the glider pilot can start looking for thermals or enjoying an acrobatic flight.   

**Components** (the list will be kept updated)
- Nvidia Jetson Nano developer board (with cuda)
- Sony IMX477 Sensor (Raspberry Pi Camera module with wide angle lens)
- Power management
- autopilot module (tbd)
- RF backlink to ground (tbd)
- Mounting and adjustment of all components (considering center of gravity)

**Project phases** (idea & project start: Feb 2021, project status: ongoing):
- Proof of concept (completed)
- Developing of first prototype (completed)
- First experimental flight to test hardware (completed)
- Finalizing AI model for tug aircraft localization (ongoing)
- Establishing connection to autopilot module
- Implementing RF backlink to glider pilot remote control
- Tests & calibration

# Idea and concept:

![Concept](https://user-images.githubusercontent.com/82274251/123086547-d5275280-d423-11eb-9df7-8a1b019ed7b5.jpeg)
Ususally RC glider and towing pilot stand close to each other on the ground in order to agree on the flight path and climbing rate. The larger the altitude, the more difficult it is for the RC glider pilot to estimate the relative position of the glider with respect to the tug aircraft and to maintain a safe flight path behind the tow plane. Any small deviation from the safe flight path for as little as a few seconds might cause massive stress on the glider and tow plane structure once the line starts to tense up and very probably force the glider pilot to disconnect immediately to avoid crash of both planes.

The idea is to use the advantages of FPV (first person view) to fly the glider accurately. Once the glider localized the tow plane (AI model running on Jetson nano) the necessary correction of the flight path (for example due to wind) is calculated onboard and used as an input to the autopilot that derives the necessary servo corrections.   

![Flight situations](https://user-images.githubusercontent.com/82274251/123089962-e3776d80-d427-11eb-95f0-0ad9560221cd.jpeg)

# Proof of concept:
Development of a first AI model to find the wingtips of the tug aircraft (red dot: left wingtip, green dot: right wingtip, black dot: middle of the wings, yellow dot: center of mass of the mask). A few hundred screenshots from online videos were used for this very first proof of concept. 

![proof of concept](https://user-images.githubusercontent.com/82274251/123097187-2b01f780-d430-11eb-90b2-64e775865dac.jpeg)

The performance was astonishing! :-) 

A pretrained FASTER R-CNN model with resnet50 backbone proposed by Facebook AI research was used to generate the masks (cf. source code for more details) and trained using the masked screenshots as training data (I spend a day drawing the training masks on ipad manually :-) ). The model was trained on Google Colab and the weights saved in order to deploy the model locally. A separated test set with about 60 images was also prepared to validate the model. The images above are taken from the test set, thus not used for training.

# Hardware & getting ready for first experimental flights
Since the results looked very promising, I started purchasing the necessary equipment. The camera driver needed to be compiled first in order to run on the Nvidia Jetson Linux board.  
A fiberglass base plate carries all components safely and is robust enough to withstand strong wind, vibrations and shocks. 

Images:

Left: Trying to install the camera driver in order to capture a first picture. Middle: Building the structure necessay to mount the experimental equipment on the plane. Right: The setup is ready for transport to the flying field.

![getting started](https://user-images.githubusercontent.com/82274251/123093988-a5307d00-d42c-11eb-8dd1-2b93edeafd0c.jpeg)

**Power supply:**
A special low loss power supply board was needed for field operation:
- ground power, fused and regulated from 12V supply 
- power from onboard battery, fused, filtered, regulated (9-20V)

Any transition between the power sources should not trigger any reboot of the system. Proper power management is necessary in order to avoid any danger with LiPo batteries! The power supply board is located between the camera and the Jetson board.

The center of gravity of the experimental board is optimized in order to align with the center of gravity of the carying airplane. 

# First flights
Everything worked out excatly as it was expected. I simply love field experiments :-)
 
Images: Configuring the system for its first flight. System is connected to ground power not to discharge onboard battery. As always, dady is my perfect assistant and ready for take-off for a first solo flight. 

![first flight](https://user-images.githubusercontent.com/82274251/123092903-4585a200-d42b-11eb-9f90-2d105afc4fab.jpeg)

Second flight with towing. 40m line and towing airplane ready (image in the middle). For safety reasons, a glider with onboard motor was chosen for this experiment. The motor never needed to be used but could have beed helpful in case something would have gone wrong. Eventough it was quite windy some good recordings could be saved. 
![second flight](https://user-images.githubusercontent.com/82274251/123091619-df4c4f80-d429-11eb-82bc-6e16b9c73797.jpeg)

# Results of first flights

The following images were recorded during the first experimental flights. 
Left image: original image. Middle image: calculated mask. Right image: Mask superposed to the image. 
![calculated masks](https://user-images.githubusercontent.com/82274251/123094952-cb0a5180-d42d-11eb-96a7-cbc98af52df5.jpeg)

## The project is ongoing and I am excited to update this page soon!
(Last update June 2021)
