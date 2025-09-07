#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 tombraid@snu.ac.kr
# All right reserved.
#

import time
import struct
import json
from pymodbus.client import ModbusTcpClient
from ksconstants import STATCODE, CMDCODE, PRIVCODE

def getobservation(reg1, reg2):
    return struct.unpack('f', struct.pack('HH', reg1, reg2))[0]

def readsensor(client, item):
    res = client.read_holding_registers(item["start-address"], count=3, device_id=item["unit"])
    if res.isError():
        print ("정보를 읽어오는데 실패했습니다.")
    else:
        reg = res.registers
        print (reg)
        if reg[2] == STATCODE.READY:
            val = getobservation(reg[0], reg[1])
            print ("{} 센서의 상태는 정상이고, 관측치는 {} 입니다.".format(item["name"], val))
        else:
            print ("{} 센서의 상태가 비정상입니다.".format(item["name"]))


# Load configuration
with open('conf.json', 'r') as f:
    config = json.load(f)

devices = [
    {"unit": 2, "start-address": 203, "name": "기상대-온도"},
    {"unit": 2, "start-address": 212, "name": "기상대-습도"},
    {"unit": 2, "start-address": 218, "name": "기상대-감우"},
    {"unit": 2, "start-address": 227, "name": "기상대-일사"},
    {"unit": 2, "start-address": 230, "name": "기상대-풍속"},
    {"unit": 2, "start-address": 233, "name": "기상대-풍향"},
    {"unit": 3, "start-address": 203, "name": "내부-온도"},
    {"unit": 3, "start-address": 212, "name": "내부-습도"},
    {"unit": 3, "start-address": 239, "name": "내부-이산화탄소"},
    {"unit": 3, "start-address": 242, "name": "배지-EC"},
    {"unit": 3, "start-address": 248, "name": "배지-함수율"},
    {"unit": 3, "start-address": 257, "name": "배지-온도"},
    {"unit": 5, "start-address": 204, "name": "양액-EC"},
    {"unit": 5, "start-address": 213, "name": "양액-pH"},
    {"unit": 5, "start-address": 225, "name": "양액-누적유량"}
]

client = ModbusTcpClient(config['modbus_ip'], port=config['modbus_port'])
client.connect()

for dev in devices:
    readsensor(client, dev)
    time.sleep(1)


"""
# 2번 유닛아이디 203번지부터 3개의 레지스터를 읽습니다. (외부 온도)
res = client.read_holding_registers(203, count=3, device_id=2)
if res.isError():
    print ("정보를 읽어오는데 실패했습니다.")
else:
    reg = res.registers
    print (reg)
    if reg[2] == STATCODE.READY:
        rad = getobservation(reg[0], reg[1])
        print ("온도 센서의 상태는 정상이고, 관측치는 {} 입니다.".format(rad))
    else:
        print ("온도 센서의 상태가 비정상입니다.")

# 3번 슬레이브 212번지부터 3개의 레지스터를 읽습니다. (습도)
res = client.read_holding_registers(212, count=3, device_id=3)
if res.isError():
    print ("정보를 읽어오는데 실패했습니다.")
else:
    reg = res.registers
    print (reg)
    if reg[2] == STATCODE.READY:
        temp = getobservation(reg[0], reg[1])
        print ("습도 센서의 상태는 정상이고, 관측치는 {} 입니다.".format(temp))
    else:
        print ("습도 센서의 상태가 비정상입니다.")

"""

