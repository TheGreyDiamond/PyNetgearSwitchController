import switch

sw = switch.NetgearSwitch(ip = "", SID="", cookieName="SID", hashN = 27016,passwordHash="") 

ports = sw.getAllPorts()
#sw.setPortState("port4","1","2")
##sw.updateDeviceInfo()
print(sw.getDeviceInfo())
for mP in ports:
    print(mP.realSpeed)
sw.logout()
