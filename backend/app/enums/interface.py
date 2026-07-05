from enum import Enum

class InterfaceType(str,Enum):
    ETHERNET="Ethernet"
    LOOPBACK="Loopback"
    VLAN="Vlan"
    PORT_CHANNEL="Port-Channel"
    TUNNEL="TUNNEL"
    
class InterfaceStatus(str,Enum):
    UP="Up"
    DOWN="Down"
    ADMIN_DOWN="Admin Down"