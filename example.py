import switch

sw = switch.NetgearSwitch(ip = "192.168.0.239", cookieName="SID", password="password", mode=2)
# Disable
# sw.setPortState("port3","2","2")
# Enable
sw.setPortState("port3","1","2")
