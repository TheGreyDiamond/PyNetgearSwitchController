import switch
#uPBEEbADOCqsij`nJCyWmNCZeZkwhlPNcF]inOMumnIPuDgapWhIK\pe^nAx_v[_CmZqgJpSLSgkcRsO           # 27016
sw = switch.NetgearSwitch(ip = "deimos.fritz.box", cookieName="SID", hashN = 27016,password="nim.busc3", mode=2) ## deimos.fritz.box

ports = sw.getAllPorts()
#sw.setPortState("port4","1","2")
##sw.updateDeviceInfo()
print(sw.getDeviceInfo())
for mP in ports:
    print(mP.realSpeed)
sw.logout()
