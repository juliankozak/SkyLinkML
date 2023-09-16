# SkyLinkML Project
**RC Glider Towing**


Idea: February 2021   
Last update and test flights: August 2023  
**Don't hesitate to contact me if you are interested in this project, I am open for any kind of collaboration**   
E-mail: [ j u l i a n k o z a k 2 [ a t ] g m a i l [ d o t ] c o m ]   
Project status: ongoing and exciting :-)   

# Introduction
![Concept](https://user-images.githubusercontent.com/82274251/123086547-d5275280-d423-11eb-9df7-8a1b019ed7b5.jpeg)
**Glider towing** is a popular way of getting large and heavy remote controlled glider planes into the air, but it is also one of the most challenging tasks for rc airplane pilots. The glider is connected to the towing aircraft with a 20m long, few millimeter thin rope that is released from the glider side once the desired altitude is reached by the two aircraft. The tow plane then usually descends and prepares for landing while the glider searches for thermals and tries to remain in the air as long as possible. 

During the entire towing process, the glider pilot needs to keep the glider precisely behind the towing aircraft. Moreover, the glider pilot must maintain the same airspeed and same climbing rate as the tow plane. This can get particular challenging at altitudes exceeding 100m above ground and tailwind or crosswind conditions. Any small deviation from the safe flight path might cause sudden stretching of the rope, stall of the towing plane or in worst case some structural damage to one or both of the planes.

Usually, the two RC pilots flying the glider and tow plane, stand close to each other and communicate about varying wind conditions, airspeed, climbing rate, flight path, visibility etc.  **The larger the altitude, the more difficult it is for the RC glider pilot to estimate the relative position of the glider with respect to the towing aircraft and to maintain a safe flight path behind the tow plane. The rope is almost invisible at these altitudes.** 

**Goal**  
Using a computer vision machine learning model to localize the tow-plane from glider perspective and try to automatically keep the glider on the optimal flight path. Automatically generate control signals for the glider remote control system to correct deviations from the flight path, but always allow the glider pilot to take over control and fly manually. Glider towing is one possible application for this project. **The same concept could also be adapted for other applications such as formation flights, windshield flights and fuel consumption analysis.** The goal of this page is to share my ideas and to find other people interested in this project. 

## System design and components
The entire system is composed of the following components:
- Two pilots, two remote controls, the tow plane and the glider (nothing new so far). 
- The glider is equipped with an onboard unit that records and transmits live images (FPV view) to the ground station with very low latency. Moreover, the onboard unit also contains a GPS receiver. 
- The ground station maintains a wireless connection with the onboard unit. The ground station is composed of an Nvidia Jetson Nano processor to deploy the computer vision model (cuda) and a PC to manage the application and show the user interface. The ground station also generates voice commands for the pilots, so there should not be any need to look a screen during flight (especially problematic during sunny days). The ground station generates an analogue signal that can be injected into the trainer module of the glider's pilot remote control. The initial concept behind the trainer mode is to teach RC flying to a student by connecting the student and teachers remote controls and flying the same airplane together. The teacher can configure in his remote which controls he wants to pass over to the student, and the teacher can take over control of the plane from the student any time. In this project, the idea is to simulate the student and to generate the student's remote control output signal by the ground station and to pass the signal to the teacher's remote control. The ground station can then fly the glider automatically but the pilot (teacher) can then take over control of the glider at any time. This is a very important safety feature necessary to comply with the regulations for flying RC airplanes.

![Concept](https://github.com/juliankozak/SkyLinkML/assets/82274251/bc8ffd57-ade1-4609-857a-dbb89a335da2)

**Hardware**

**Onboard unit:**
- Camera with Sony IMX477 Sensor, wide-angle lens with manual focus and exposure control
- ublox GPS receiver
- Raspberry Pi Zero (as a small processor inside the onboard unit)
- AX1800 Wifi module with **antenna diversity** and Linux driver for Raspberry Pi. Antenna diversity is absolutely needed to maintain a stable link in all flight directions given the radiation pattern of the used antennas. In order to avoid any interference with the remote control performing frequency hopping in the 2,4GHz ISM band, the system operates the 5,8GHz ISM band. The connection is a pure line-of-sight link and the increased propagation loss caused by the higher frequency is accepted. This approach feels safer since the rather large bandwidth occupied by the data channel might block many of the frequency hopping channels used by the remote control (but these are assumptions, some measurements or vendor information would be needed to confirm). 
- power management 

**Ground station:**
- Nvidia Jetson Nano developer board
- Laptop for GUI and application management
- Power management (able to switch between different power sources without interruption)
- AC1900 long range wireless router (TP-Link)

Note: I am aware that there are more suitable and professional components on the market that would perform better, be smaller and more efficient. However, I decided for a trade-off between cost, availability and ease of use for this prototype.

**Project phases**
- Proof of concept (*completed*)
- Getting hardware ready for first prototype (*completed*)
- First experimental flight to test hardware (*completed*)
- Second generation of camera mount (*completed*)
- Training AI model for tow-plane localization (*ongoing*)
- Implementing system components, integrating AI model (*ongoing*)
- Localizing tow-plane from glider perspective, generating voice commands (*ongoing*)
- Generating control signals for glider remote control (*planned*)
- Test flights for every step to account for practical aspects relevant outdoor in the field.  


**The idea is to use the advantages of FPV (first person view) to fly the glider accurately.** Typical flight situations are shown in the following image.
![Flight situations](https://user-images.githubusercontent.com/82274251/123543403-84c73200-d74e-11eb-8230-85fb4ff22b03.jpeg)


# Proof of concept (AI model)
Development of a first AI model to localize the wingtips of the tug aircraft. A few hundred screenshots from online videos were used for this very first proof of concept since no other data was available at that time.

A pretrained FASTER R-CNN model with resnet50 backbone proposed by Facebook AI research was used to generate masks and trained using the masked screenshots as training data (I spend a day drawing the training masks on ipad manually :-) ). The model was trained on Google Colab and the weights saved in order to deploy the model locally. A separated test set was also prepared to validate the model. The images below are taken from the test set, thus not used for training. The AI model generates a masks, the wingtips were derived from the mask in a second step with traditional cv methods (red and green dots). 

**The performance was astonishing! :-)** 

![proof of concept](https://user-images.githubusercontent.com/82274251/123097187-2b01f780-d430-11eb-90b2-64e775865dac.jpeg)

**Image:** Illustration of first proof of concept
(**red dot:** left wingtip, **green dot:** right wingtip, **black dot:** middle of the wings, **yellow dot:** center of mass of the mask)

# Hardware and First Experimental Flights

Since the results looked very promising, I started purchasing the necessary hardware. The first step was to get the equipment run, to fix the camera driver issues, install all dependencies, and so on. 
Soon it became obvious that a stable and lightweight frame is needed to mount the equipment safely on the plane. A fiberglass plate carries all components and is robust enough to withstand wind, vibrations and shocks. 

![getting started](https://user-images.githubusercontent.com/82274251/123093988-a5307d00-d42c-11eb-8dd1-2b93edeafd0c.jpeg)

**Left image:** First experiments to capture a picture and getting familiar with the camera focus and exposure settings. **Middle image:** Building the frame necessary to mount the equipment on the plane. **Right image:** The setup is ready for transport to the flying field!

**Power supply:**
A special low loss power supply board was needed for field operation:
- ground power, fused and regulated from 12V supply 
- power from onboard lithium polymer battery, fused, filtered, regulated (9-20V)
Transition between power sources should be possible without any interruption of the system.

The center of gravity of the experimental board is optimized in order to align with the center of gravity of the airplane. 

# First flights
Surprisingly everything worked out as it was expected. I simply love field experiments :-)

**Flight 1:** Solo flight without towing, getting familiar with the extra load!
![first flight](https://user-images.githubusercontent.com/82274251/123092903-4585a200-d42b-11eb-9f90-2d105afc4fab.jpeg)

System is connected to ground power not to discharge onboard battery while preparing the flight. **Right image:** As always, my dad is my perfect assistant and ready for take-off for the first solo flight. 

**Flight 2:** Second flight with towing. 

Towing airplane and 20m tow-rope are ready (image in the middle). For safety reasons, a glider with onboard motor was chosen for this experiment. Even-tough it was quite windy, we made some good recordings. 
![second flight](https://user-images.githubusercontent.com/82274251/123091619-df4c4f80-d429-11eb-82bc-6e16b9c73797.jpeg)

### Results of first flights

The following images were recorded during flight 2 and processed offline after the flight. 
Left image: original image. Middle image: calculated mask. Right image: Mask superposed on the image. 
![calculated masks](https://user-images.githubusercontent.com/82274251/123094952-cb0a5180-d42d-11eb-96a7-cbc98af52df5.jpeg)

## Second generation of camera mount
Initially, the goal was to put as little effort as possible into  hardware design and to get a flyable system as soon as possible. Based on the lessons learned from the first generation, the system design was updated. The main changes were:
- Since a stable wireless link between onboard unit and ground station can be achieved,
- Jetson Nano can remain on the ground, reducing weight, volume and energy consumption of the onboard unit,
- a Raspberry Pi Zero was chosen as a small processor,
- a GPS module was added to the onboard unit
- MIMO antenna system was added to the onboard unit
- a flexible power supply with filtering was added to the onboard unit,
- the onboard unit was designed to be compact and easily mountable on different airplanes.

The following image shows the updated design of the onboard unit. Most of the electronic components are packed into the baseplate and into the shaft of the frame keeping the center of mass as low as possible. Only the camera and the GPS receiver are placed in the gondola. The unit is nicely balanced and can be mounted onto the plane while keeping the center of gravities aligned.  

**The new look of the onboard unit:**  
![camera-bird-eye-prototype](https://github.com/juliankozak/SkyLinkML/assets/82274251/2ada56be-d733-4f03-8cf9-5fed1d6ae390)

The following images were recorded during one of the flights. The following two points could be clarified: The tow-plane remains within the frame from take-off until separation, meaning that the selected wide angle camera lens is suitable for this application. And, the tow plane can be identified and is not too small on the picture.

![flight_images_bird_eye_150dpi](https://github.com/juliankozak/SkyLinkML/assets/82274251/b2eb4384-8038-4a9b-a17c-3d2da84af5c4)

## Signal quality:

During all flights, GPS data and wireless signal parameters are constantly logged as a background job. The logfile is saved on the onboard unit and can be downloaded after landing for further analysis in case of unexpected signal outages. **Antenna diversity is absolutely necessary** for reliable wireless connection. The two antennas should be oriented as orthogonal as possible to each other in order to have appropriate gain in all directions.

![link_quality](https://github.com/juliankozak/SkyLinkML/assets/82274251/56342453-5717-4263-9162-d1a48f7eaa8a)

-> No signal outages were noticed in practice so far on the flight site. 

## The project is ongoing, and I am excited to update this page soon!

Current thoughts:
- It seems that the horizon can be used as a reference and no additional gyroscopic sensors are needed.
- Voice output is really important to keep the pilot focused on the flight and not on the screen.
- 100ms total latency are my target, but it is challenging.
- Trying pose estimation with Perspective-n-Point (PnP) pose computation.

Note: The goal of this page is to describe the approach and to share my ideas. The source code is very hardware specific and I did not include it here. Please contact me if you are interested in this project.
(Last update August 2023)

# Continuation
Keeping airplanes precisely close to each other in the air without tow-rope. This can be useful for windshield analysis or for formation flights. 


**Looking for collaboration with other enthusiastic and wonderful people**