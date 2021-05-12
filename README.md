# PyNetgearSwitchController
 
A Python library to control Netgear ProSafe Switches.
 This is still under heavy development and should not be used in a production envoriment.
 
# Documentation
First of all you need to create a switch object:
```py
sw = switch.NetgearSwitch(ip = "<your switch ip>", SID="", cookieName="SID", hashN = 27016, passwordHash="<your password hash>", mode=2)
```
To generate the passwordHash use passwordGen.html, just enter your password and retrieve the randomcode.
You can retrieve all port info by using `sw.getAllPorts()`, it will return a list of port objects. Taking a look at the port object:
```python
class port():
    def __init__(self):
        self.name = ""
        self.state = "unset"
        self.speed = "unset"
        self.realSpeed = "unset"
        self.flow = "unset"
        self.maxMTU = "unset"
```
You can see which atributes can be retrieved. You can also retrieve device information with `sw.getDeviceInfo()`, this will return a dictonary with info about the switch.
Here is an full example:
```python
import switch

sw = switch.NetgearSwitch(ip = "<your switch ip>", SID="", cookieName="SID", hashN = 27016, passwordHash="<your password hash>", mode=2)

ports = sw.getAllPorts()
sw.updatePorts()             # Forces a port state update
print(sw.getDeviceInfo())    # Prints out info about the switch
for mP in ports:
    print(mP.realSpeed)
sw.logout()

```
It will output all linked speeds.

---
**Warning**

Always use sw.logout() or the next login might fail!

---

# Troubleshooting
If you get an error try using another mode:
| Mode | Devices         |
|------|-----------------|
| 1    |  Unknown        |
| 2    | GS108Ev3[Works] GS105Ev2[Works] |

If that dosn't change the cookieName. You can retrieve it easily, here's a quick guide:
1. Open Firefox and navigate to your switch's login page. Then login.
2. RightClick, then select "Inspect Element"
3. Now click on the tab "Storage" and open the "Cookie" dropdown
4. Note down the Name of the cookie, and set cookieName to it
![Guide](https://github.com/TheGreyDiamond/PyNetgearSwitchController/blob/master/netgearSwitch.png)

# All functions
## Switch
`updatePorts()`
   Forces an update of all ports
   
`updateDeviceInfo()`
   Forces an update of device info atributes
   
`getAllPorts()`
   Returns all ports of the switch
   
`getPortByNo(num)`
   Gets one ports by its number
   
`getDeviceInfo()`
   Returns all device information
   
`getDevicePropByName(name)`
   Returns device information by property name
   
`setPortState(portName, speed, flow)`
   Sets the port properties
  
