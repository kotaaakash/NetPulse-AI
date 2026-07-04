from enum import Enum
class DeviceVendor(str,Enum):
    CISCO = "Cisco"
    JUNIPER = "Juniper"
    ARISTA = "Arista"
    PALO_ALTO = "Palo Alto"
    FORTINET = "Fortinet"


class DeviceType(str, Enum):
    ROUTER = "Router"
    SWITCH = "Switch"
    FIREWALL = "Firewall"
    LOAD_BALANCER = "Load Balancer"
    WIRELESS_CONTROLLER = "Wireless Controller"


class DeviceStatus(str, Enum):
    HEALTHY = "Healthy"
    DOWN = "Down"
    MAINTENANCE = "Maintenance"
    UNKNOWN = "Unknown"