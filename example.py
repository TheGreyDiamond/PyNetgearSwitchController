import switch

sw = switch.NetgearSwitch(ip = "", cookieName="SID", hashN = 27016, password="") 

ports = sw.getAllPorts()
#sw.setPortState("port4","1","2")
##sw.updateDeviceInfo()
print(sw.getDeviceInfo())
for mP in ports:
    print(mP.realSpeed)
sw.logout()
