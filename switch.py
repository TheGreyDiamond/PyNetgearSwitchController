import requests
import hashlib

def removeEmptiesFromList(li):
    ## Remove empty elements
    errord = False
    while(not errord):
        try:
            li.remove('')
        except ValueError:
            errord = True
    ## Remove kinda empty elements
    errord = False
    while(not errord):
        try:
            li.remove(' ')
        except ValueError:
            errord = True
    errord = False
    while(not errord):
        try:
            li.remove('  ')
        except ValueError:
            errord = True
    return(li)
                

class NetgearSwitch():
    def __init__(self, ip,SID, hashN, passwordHash, cookieName = "SID", mode=1):
        headers = {'User-Agent': 'Mozilla/5.0','Content-Type':'application/x-www-form-urlencoded'}
        payload = {'password':passwordHash}
        try:
            r2 = requests.post('http://' + ip + '/login.cgi', headers=headers, data=payload )
        except:
            raise Exception("Unknow host")
        #print(r2.cookies)
        self.__cookies__ = {cookieName: r2.cookies[cookieName]}
        self.__ports__ = []
        self.ip = ip
        self.__mode__ = mode
        self.__hash__ = hashN
        
        
        
        self.deviceInfo = {}
        #self.logout()
        self.updatePorts()
        self.updateDeviceInfo()
        #self.logout()
        #

    def splitE(self, word): 
        return [char for char in word]
   

    def updatePorts(self):
        if(self.__mode__ == 1):
            r = requests.post('http://' + self.ip + '/status.htm', cookies=self.__cookies__)
        elif(self.__mode__ == 2):
            r = requests.post('http://' + self.ip + '/status.cgi', cookies=self.__cookies__)
        pro = r.text
        print(pro)
        pro = pro.split('<tr><td class="topTitleBottomBar" colspan="2"></td></tr>')[1]
        pro = pro.split('''       </table>
              </td>
             </tr>
            </table>
           </td>
          </tr>
         </table>
        </form>''')[0]
        pro = pro.split("<tr class=\"portID\"><td class=\"def firstCol def_center\"><input class=\"checkbox\" type=\"checkbox\" name=")
        i = 1
        self.__ports__ = []
        while(i< len(pro)):
            t = pro[i]
            i2 = 0
            temp = t.split("\"")[20]
            temp2 = t.split("\"")[28]
            temp3 = t.split("\"")[44]
            myPort = port()
            myPort.name = t.split("\"")[1]
            myPort.state = t.split("\"")[20][1:len(temp)-20].upper()
            myPort.speed = t.split("\"")[28][1:len(temp2)-20]
            myPort.realSpeed = t.split("\"")[39]
            myPort.flow = t.split("\"")[44][1:len(temp3)-20].upper()
            try:
                myPort.maxMTU = t.split("\"")[57]
            except IndexError:
                print("Failed to get MAX mtu")
            self.__ports__.append(myPort)
            i+=1

    def getAllPorts(self):
        return(self.__ports__)

    def getPortByNo(self, num):
        return(self.__ports__[num])

    def updateDeviceInfo(self):
        if(self.__mode__ == 1):
            r = requests.post('http://' + self.ip + '/switch_info.htm', cookies=self.__cookies__)
        elif(self.__mode__ == 2):
            r = requests.post('http://' + self.ip + '/switch_info.cgi', cookies=self.__cookies__)
            
        pro = r.text
        #print(pro)
        if(self.__mode__ == 2):
            pro = pro.split("<tr><td class=\"paddingTableBody\" colspan='2'><table class=\"tableStyle\" id=\"tbl2\" style=\"width:728px;\">")[1]
            pro = pro.split("<input type=hidden name='err_msg' id='err_msg' value='' disabled>")[0]
            pro = pro.split("<tr>")
            dataT = {}
            i2 = 0
            while(i2 <  len(pro)):
                pro[i2] = pro[i2].replace("d nowrap='' width='300'>","")
                pro[i2] = pro[i2].replace("<td class=\"padding14Top\">","")
                pro[i2] = pro[i2].replace("</td>","")
                pro[i2] = pro[i2].replace("</tr>","")
                pro[i2] = pro[i2].replace("<td  align=\"center\" nowrap>","")
                pro[i2] = pro[i2].replace("<td width='300' class=\"padding14Top\">","")
                if(len(pro[i2].split("\n"))>2):
                    temData = pro[i2].split("\n")
                    temData = removeEmptiesFromList(temData)
                    if(temData[0][2:] != "Switch Name" and temData[0][2:] != "DHCP Mode" and temData[0][2:] != "IP Address" and temData[0][2:] != "Subnet Mask" and temData[0][2:] != "Gateway Address"):
                        dataT[temData[0][2:]] = temData[1][2:]
                    else:
                        temData[1] = temData[1].replace("<input type=\"text\" name=\"","")
                        temData[1] = temData[1].replace("\"","")
                        temData[1] = temData[1].replace("id=","")
                        if(temData[0][2:] == "Switch Name"):
                            temData[1] = temData[1][32:temData[1].index("size=")]
                            dataT[temData[0][2:]] = temData[1]
                        elif(temData[0][2:] == "DHCP Mode"):
                            #print(str(temData) + " ID: " + str(i2) + " WITH len: " + str(len(temData)))
                            temData[5] =  temData[5].replace("  <input type=\"checkbox\" id=\"refresh\" name=\"refresh\" value=\"","")
                            temData[5] = temData[5].split("\"")[0]
                            dataT[temData[0][2:]] = temData[5]
                            #print(temData[5])
                        else:
                            print("!! NO HANDEL FOUND !! " + str(temData) + " ID: " + str(i2) + " WITH len: " + str(len(temData)))
                i2+=1
            self.deviceInfo = dataT
        elif(self.__mode__ == 1):
            pro = pro.split("<tr><td class=\"paddingTableBody\" colspan=\"2\"><table class=\"tableStyle\" id=\"tbl1\" style='width:745px;'> ")[1]
            pro = pro.split("<input type=hidden name='err_msg' id='err_msg' value='' disabled>")[0]
            pro = pro.split("<tr>")
            dataT = {}
            i2 = 0
            while(i2 <  len(pro)):
                
                pro[i2] = pro[i2].replace("<td nowrap='' width='300'>","")
                pro[i2] = pro[i2].replace("<td nowrap='' align='center'>","")
                pro[i2] = pro[i2].replace("</td>","")
                pro[i2] = pro[i2].replace("</tr>","")
                pro[i2] = pro[i2].replace("<td  align=\"center\" nowrap>","")
                pro[i2] = pro[i2].replace("<td width='300' class=\"padding14Top\">","")

                print("ID: " + str(i2) + " " + pro[i2])
                
                if(len(pro[i2].split("\n"))>2):
                    temData = pro[i2].split("\n")
                    temData = removeEmptiesFromList(temData)
                    if(temData[0][2:] != "Switch Name" and temData[0][2:] != "DHCP Mode" and temData[0][2:] != "IP Address" and temData[0][2:] != "Subnet Mask" and temData[0][2:] != "Gateway Address"):
                        dataT[temData[0]] = temData[1]
                    else:
                        temData[1] = temData[1].replace("<input type=\"text\" name=\"","")
                        temData[1] = temData[1].replace("\"","")
                        temData[1] = temData[1].replace("id=","")
                        if(temData[0][2:] == "Switch Name"):
                            temData[1] = temData[1][32:temData[1].index("size=")]
                            dataT[temData[0][2:]] = temData[1]
                        elif(temData[0][2:] == "DHCP Mode"):
                            #print(str(temData) + " ID: " + str(i2) + " WITH len: " + str(len(temData)))
                            temData[5] =  temData[5].replace("  <input type=\"checkbox\" id=\"refresh\" name=\"refresh\" value=\"","")
                            temData[5] = temData[5].split("\"")[0]
                            dataT[temData[0][2:]] = temData[5]
                            #print(temData[5])
                        else:
                            print("!! NO HANDEL FOUND !! " + str(temData) + " ID: " + str(i2) + " WITH len: " + str(len(temData)))
                i2+=1
            self.deviceInfo = dataT
        print(dataT)
        
    def getDeviceInfo(self):
        return(self.deviceInfo)
    
    def getDevicePropByName(self, name):
        return(self.deviceInfo[name])

    def setPortState(self, portName, speed, flow):
        speedTable = {
            "Auto": 1,
            "Disable": 2,
            "10M Half": 3,
            "10M Full": 4,
            "100M Half": 5,
            "100M Full": 6}
        pI = 0
        try:
            pI = int(speed)
        except ValueError:
            speed = speedTable[speed]
        
        
        if(self.__mode__ == 1):
            headers = {'User-Agent': 'Mozilla/5.0','Content-Type':'application/x-www-form-urlencoded'}
            payload = {'SPEED':speed,'FLOW_CONTROL':flow,portName:'checked','hash':self.__hash__}
            r2 = requests.post('http://' + self.ip + '/status.cgi', cookies=self.__cookies__,headers=headers,data=payload )
        else:
            r2 = requests.post('http://' + self.ip + '/status.cgi&SPEED=' + str(speed) + '&FLOW_CONTROL=' + flow +'&' + portName + '=checked&hash=' + self.__hash__, cookies=self.__cookies__)
        print(r2.text)
        
        r2.close() 
    def logout(self):
        print("Logging off")
        r = requests.post('http://' + self.ip + '/logout.cgi', cookies=self.__cookies__)
 
    
class port():
    def __init__(self):
        self.name = ""
        self.state = "unset"
        self.speed = "unset"
        self.realSpeed = "unset"
        self.flow = "unset"
        self.maxMTU = "unset"


