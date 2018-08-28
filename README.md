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
