# Smart-Health-Mirror: Kinect-Module

This service is responsible for providing 3D skeletal joint data for the [Smart Health Mirror framework](https://github.com/JohannaLatt/Master-Thesis-Smart-Health-Mirror). The framework is currently optmized to be run with a Microsoft Kinect v2. 

The repository includes a simple C#-program that streams the Kinect 3D data to the [server](https://github.com/JohannaLatt/SHM-Server/tree/master) via the messaging service. To use other tracking systems, a similar plugin would have to be written that is compatible with the messaging service and that sends the data to the server. Ideally the data is sent in the format currently used throughout the serve infrastructure:

```
{
  'SpineBase': [331.2435, -419.485077, 2150.36621], 
  'SpineMid': [313.7696, -185.470459, 1992.33936], 
  'Neck': [294.341644, 44.1935768, 1821.40552], 
  'Head': [301.3063, 171.161179, 1819.05847], ...
 }
```

This format equals the joints provided by the Kinect v2. The [server](https://github.com/JohannaLatt/SHM-Server/tree/master) can also handle other formats, however, additional preprocessing will be required on the server-side.

Furthermore, the framework includes a python program that can simulate a Kinect in case no real Kinect is available. The simulation program already includes some samples, but the logging-data created by the [server](https://github.com/JohannaLatt/SHM-Server/tree/master) can also be directly fed into the simulator. The simulator can be started and paused using `t` (track) and `p` (pause). The file to be used can be specified with the `-f`-flag (specify the whole name of the file including the extension).

## Installation

### Kinect
To run the actual Kinect, connect it to your Windows computer after having installed the [Windows Kinect v2 SDK] (https://www.microsoft.com/en-us/download/details.aspx?id=44561). Make sure it is recognized. Then just double-click [KinectStreaming.exe](https://github.com/JohannaLatt/Smart-Health-Mirror/blob/master/Kinect/Windows/KinectStreaming/bin/Release/KinectStreaming.exe). The command line prompt that opens expects you to enter the IP address of the RabbitMQ server (without the port). Enter the IP address (or just enter `localhost`) and press enter. The program should then automatically connect to the messaging-service and to the Kinect and start streaming data (which will also be displayed in the prompt).

### Kinect Simulator
Alternatively to using an actual tracking device, the simulator can also be used:

1. Make sure to have the necessary requirements installed: `pip install -r [link to requirements.txt in Simulator folder]` (if you use virtual environments, make sure to activate it)
2. Go to the Kinect Simulator-folder in this repository: `cd Kinect/Simulator`
3. Update the RabbitMQ-messaging-server-ip in the [config-file](https://github.com/JohannaLatt/Smart-Health-Mirror/blob/master/Kinect/config/kinect_config.ini) if needed
4. Start the simulator
```
python index.py -s [stanford, cornell] -f [filename including extension]
``` 
5. Enter `t` and press enter to start the tracking simulation, `p` stops the simulation and `q` quits the simulator
6. To use data recorded with this framework as the basis for the simulator, take the log-file created by the server (it will be under /Server/Server/logs) and copy it into /Kinect/data/sample-kinect. Let's assume the file is named `tracking-data.log`. To use this data with the simulator, start it with: `python index.py -f tracking-data.log`. 
