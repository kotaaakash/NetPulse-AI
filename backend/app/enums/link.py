from enum import Enum


class LinkType(str, Enum):
    COPPER = "Copper"
    FIBER = "Fiber"
    DAC = "DAC"
    WIRELESS = "Wireless"
    VIRTUAL = "Virtual"
    
class LinkStatus(str, Enum):
    UP = "Up"
    DOWN = "Down"
    DISABLED = "Disabled"