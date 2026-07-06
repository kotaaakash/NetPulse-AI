from enum import Enum


class ConfigurationType(str, Enum):
    RUNNING = "Running"
    STARTUP = "Startup"