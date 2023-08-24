# SkyLinkML Project
Idea & project start: February 2021   
Last update and test flights: August 2023  
Project status: ongoing

# Concept for RC flights 
![Concept](https://user-images.githubusercontent.com/82274251/123086547-d5275280-d423-11eb-9df7-8a1b019ed7b5.jpeg)
**Glider towing** is a popular way of getting large and heavy glider planes into the air, but it is also one of the most challenging tasks for remote controlled airplane pilots. The glider is connected to the towing aircraft with a 20m long, few millimeter thin rope that is released from the glider once the desired altitude was reached by the two aircraft. The tow plane then usually descends and prepares for landing while the glider looks for thermals in order to remain in the air as long as possible. 

During the entire towing process, the glider pilot needs to keep the glider in a precise position behind the towing aircraft. Moreover, the glider pilot must maintain the same speed and same climbing rate as the tow plane. This can get particulary challenging at atlitudes exceeding 100m above ground and tailwind conditions during flight. Any small deviation from the safe flight path might cause the rope to break, stall of the towing plane or in worst case some structural damage to one or both of the planes (especially if the rope stretches abruptly).

Usually, the two RC pilots, flying the glider and tow plane respectively, are standing close to each other and trying to communicate about varying wind conditions, airspeed, climbing rate, flight path, visibility etc.  **The larger the altitude, the more difficult it is for the RC glider pilot to estimate the relative position of the glider with respect to the towing aircraft and to maintain a safe flight path behind the tow plane. The rope is almost invisible at these altitudes.** 

**Goal**  
Using a computer vision machine learning model, the glider localizes his tow-plane and tries to automatically stay on the optimal flight path behind the towing aircraft until they reached the desired altitude. Glider towing is one possible application for this project. The same concept can be used for other applications such as formation flights, windshield or fuel consumption analysis.


**System design and components**  
![System overview](https://github.com/juliankozak/SkyLinkML/blob/main/images/Concept.png)

--> IMAGE


**Project phases**
- Proof of concept (*completed*)
- Purchasing hardware and getting it ready for first prototype (*completed*)
- First experimental flight to test hardware (*completed*)
- Finalizing AI model for tow-plane localization (*ongoing*)
- Establishing connection to autopilot module
- Implementing RF backlink to glider pilot remote control
- Tests & calibration



**Components** (the list will be kept updated)
- Nvidia Jetson Nano developer board to deploy the AI model
- Camera with Sony IMX477 Sensor (Raspberry Pi Camera module with wide-angle lens)
- Power management (able to switch between ground power and power from onboard battery without interruption)
- Lightweight mounting frame for all the equipment (considering center of gravity)
- RF backlink to ground (tbd)
- autopilot module (tbd)





**The idea is to use the advantages of FPV (first person view) to fly the glider automatically accurately.** Once the glider localized the tow plane the necessary correction of the flight path (for example due to wind) is calculated onboard and used as an input to the autopilot that derives the necessary servo corrections.   

Typical flight situations during towing:
![Flight situations](https://user-images.githubusercontent.com/82274251/123543403-84c73200-d74e-11eb-8230-85fb4ff22b03.jpeg)


# Proof of concept (AI model)
Development of a first AI model to find the wingtips of the tug aircraft. A few hundred screenshots from online videos were used for this very first proof of concept since no other data was available at that time.

A pretrained FASTER R-CNN model with resnet50 backbone proposed by Facebook AI research was used to generate the masks (cf. source code for more details) and trained using the masked screenshots as training data (I spend a day drawing the training masks on ipad manually :-) ). The model was trained on Google Colab and the weights saved in order to deploy the model locally. A separated test set with about 60 images was also prepared to validate the model. The images below are taken from the test set, thus not used for training. The AI model generates a masks, the wingtips are derived from the mask in a second step. 

**The performance was astonishing! :-)** 

![proof of concept](https://user-images.githubusercontent.com/82274251/123097187-2b01f780-d430-11eb-90b2-64e775865dac.jpeg)

**Image:** Illustration of first proof of concept
(**red dot:** left wingtip, **green dot:** right wingtip, **black dot:** middle of the wings, **yellow dot:** center of mass of the mask)

# Hardware & getting ready for first experimental flights

Since the results looked very promising, I started purchasing the necessary equipment. The first step was to get the equipment run, to fix the camera driver issues, install all dependencies, docker and so on. 
Soon it became obvious that a stable and lightweight frame is needed to mount the equipment safely on the plane. A fiberglass base plate carries all components safely and is robust enough to withstand strong wind, vibrations and shocks. 

![getting started](https://user-images.githubusercontent.com/82274251/123093988-a5307d00-d42c-11eb-8dd1-2b93edeafd0c.jpeg)

**Left image:** First experiments to capture a picture and getting familiar with the camera focus and exposure settings. **Middle image:** Building the frame necessary to mount the equipment on the plane. **Right image:** The setup is ready for transport to the flying field!

**Power supply:**
A special low loss power supply board (designed for 10W) was needed for field operation:
- ground power, fused and regulated from 12V supply 
- power from onboard battery, fused, filtered, regulated (9-20V)

A transition between the power sources shall no cause any reboot of the system. Proper power management is necessary in order to avoid any **danger with LiPo batteries!** The small power supply board is located between the camera and the Jetson board.

The center of gravity of the experimental board is optimized in order to align with the center of gravity of the carying airplane. 

# First flights
Everything worked out excatly as it was expected. I simply love field experiments :-)

**Flight 1:** Solo flight without towing, getting familiar with the extra load!
![first flight](https://user-images.githubusercontent.com/82274251/123092903-4585a200-d42b-11eb-9f90-2d105afc4fab.jpeg)

System is connected to ground power not to discharge onboard battery while preparing the flight. **Right image:** As always, dady is my perfect assistant and ready for take-off for a first solo flight. 

**Flight 2:** Second flight with towing. 

Towing airplane and 20m tow-rope are ready (image in the middle). For safety reasons, a glider with onboard motor was chosen for this experiment. The motor never needed to be used but could have beed helpful in case something would have gone wrong. Eventough it was quite windy, we made some good recordings. 
![second flight](https://user-images.githubusercontent.com/82274251/123091619-df4c4f80-d429-11eb-82bc-6e16b9c73797.jpeg)

### Results of first flights

The following images were recorded during flight 2. 
Left image: original image. Middle image: calculated mask. Right image: Mask superposed on the image. 
![calculated masks](https://user-images.githubusercontent.com/82274251/123094952-cb0a5180-d42d-11eb-96a7-cbc98af52df5.jpeg)

## Second generation of camera mount

--> PHOTO BIRD EYE
--> photo phoenix
--> photo GUI
--> GPS logging altitude
--> wireless signal strength
--> 3 photos from flight

GPS module was added. 
The focal length of the camera lens turned is ok.
The tow plane remained nicely within the picture.
It seems that the horizon can be used as a reference and no additional gyroscopic sensors are needed.
center of gravity

decision to continue flying experimental flights with rather small foam airplanes even though the camera load is (easier to repair in case of damage) than with larger gliders and more powerful tow planes.

## The project is ongoing, and I am excited to update this page soon!
(Last update August 2023)

# Continuation
Keeping airplanes precisely close to each other in the air without tow-rope. This can be useful for windshield analysis or for formation flights. 
