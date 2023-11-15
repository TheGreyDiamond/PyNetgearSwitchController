import switch

sw = switch.NetgearSwitch(ip = "192.168.0.239", cookieName="SID", password="Skynode0", mode=2)
# Disable
sw.setPortState(3, turnOn=False)
# Enable
sw.setPortState(3)
