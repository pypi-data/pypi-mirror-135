# from typing import Literal
from datetime import timedelta
from Adafruit_BBIO.GPIO import HIGH, LOW, BOTH, FALLING
from typing_extensions import Literal

BONEIO = "boneIO"


# MISCELLANEOUS CONSTS
RELAY = "relay"
ON = "ON"
OFF = "OFF"
STATE = "state"
ENABLED = "enabled"
OUTPUT = "output"
PIN = "pin"
ID = "id"
KIND = "kind"
GPIO = "gpio"
ACTIONS = "actions"
ACTION = "action"
OUTPUT = "output"
SWITCH = "switch"
CONFIG_PIN = "/usr/bin/config-pin"
UPDATE_INTERVAL = "update_interval"
ADC = "adc"
IP = "ip"
MASK = "mask"
MAC = "mac"
NONE = "none"
MODBUS = "modbus"
UART = "uart"
RX = "rx"
TX = "tx"

UARTS = {
    "uart1": {ID: "/dev/ttyS1", TX: "P9.24", RX: "P9.26"},
    "uart4": {ID: "/dev/ttyS4", TX: "P9.13", RX: "P9.11"},
}

# TIMINGS FOR BUTTONS
DEBOUNCE_DURATION = timedelta(seconds=0.2)
LONG_PRESS_DURATION = timedelta(seconds=0.7)
DELAY_DURATION = 0.1
SECOND_DELAY_DURATION = 0.3

# HA CONSTS
HOMEASSISTANT = "homeassistant"
HA_DISCOVERY = "ha_discovery"
HA_TYPE = "ha_type"
OUTPUT_TYPE = "output_type"
SHOW_HA = "show_in_ha"

# OLED CONST
OLED = "oled"
FONTS = "fonts"
OLED_PIN = "P9_41"
GIGABYTE = 1073741824
MEGABYTE = 1048576
WIDTH = 128
UPTIME = "uptime"
NETWORK = "network"
CPU = "cpu"
DISK = "disk"
MEMORY = "memory"
SWAP = "swap"
WHITE = "white"

# INPUT CONST
INPUT = "input"
SINGLE = "single"
DOUBLE = "double"
LONG = "long"
PRESSED = "pressed"
RELEASED = "released"


# MQTT CONST
PAHO = "paho.mqtt.client"
PYMODBUS = "pymodbus"
MQTT = "mqtt"
HOST = "host"
USERNAME = "username"
PASSWORD = "password"
ONLINE = "online"
OFFLINE = "offline"
TOPIC_PREFIX = "topic_prefix"

# I2C and MCP CONST
ADDRESS = "address"
MCP23017 = "mcp23017"
MCP = "mcp"
MCP_ID = "mcp_id"
INIT_SLEEP = "init_sleep"

# SENSOR CONST
TEMPERATURE = "temperature"
SENSOR = "sensor"
BINARY_SENSOR = "binary_sensor"
LM75 = "lm75"
MCP_TEMP_9808 = "mcp9808"
INPUT_SENSOR = "inputsensor"
SDM630 = "sdm630"

BASE = "base"
LENGTH = "length"
REGISTERS = "registers"

# TYPING
ClickTypes = Literal[SINGLE, DOUBLE, LONG, PRESSED, RELEASED]
OledDataTypes = Literal[UPTIME, NETWORK, CPU, DISK, MEMORY, SWAP, OUTPUT]
Gpio_States = Literal[HIGH, LOW]
Gpio_Edges = Literal[BOTH, FALLING]
InputTypes = Literal[INPUT, INPUT_SENSOR]
