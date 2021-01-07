# sr201-mqtt  
  
**MQTT to SR201 module interface.**  

The sr-201 is a network connected 2 channel relay module. This code is designed to 
allow it to be controlled from commands passed via MQTT (https://mqtt.org/).

Sometimes this module is described as http controlled, this is *not* the case, 
it does not contain a web server, it is controlled by sending codes to a tcp (or udp) port.
You cannot point your web browser to it directly.

![image info](./pictures/image.png)


This code draws heavily on the sr-201 code from Cryxli in Github   
(https://github.com/cryxli/sr201) and examples of MQTT in Python   
from 'Steve' (http://www.steves-internet-guide.com).  
  
This code is configured from a config file which is itself, Python,   
this allows easy import of parameters. All the parameters I think you   
should need to change are in this file. Please send me a message if   
this is not the case.  
  
The MQTT topic does not *have* to correspond to the sr-201 channel,  
but in practice it would probably be best to have these correspond   
for ease of use.  
  
Valid commands are:-  

	 # 00 Obtain relay status, toggles nothing. 
	 # 11 Turn relay 1 on 
	 # 21 Turn relay 1 off 
	 # 12 Turn relay 2 on 
	 # 22 Turn relay 2 off  

Currently the '00' code to retrieve status is not implemented.  
  
  
**To Do:-**  
1. Support MQTT topic which requires username and password  
2. Support MQTT encryption
