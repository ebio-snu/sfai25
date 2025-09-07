#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 tombraid@snu.ac.kr
# All right reserved.
#
import time
import struct
import json
from pymodbus.client import ModbusTcpClient
from ksconstants import STATCODE, CMDCODE, PRIVCODE

class NutSupplyTester:
    def __init__(self, ip, port):
        self.client = ModbusTcpClient(ip, port=port)
        self.client.connect()
        self.opid = 1
        self.ec = 0.0
        self.ph = 0.0

    def get_command_name(self, cmd):
        ctbl = {
            CMDCODE.OFF: "중지",
            CMDCODE.ONCE_WATER: "1회관수",
            CMDCODE.JUST_WATER: "원수관수",
            CMDCODE.NUT_WATER: "양액관수"
        }
        return ctbl.get(cmd, "없는 명령")

    def send_command(self, cmd, sec=None, ec=None, ph=None):
        self.opid += 1
        reg = []

        if cmd == CMDCODE.JUST_WATER:
            reg = [cmd, self.opid, 1, 1]
            reg.extend(struct.unpack('HH', struct.pack('i', sec)))
        elif cmd == CMDCODE.NUT_WATER:
            reg = [cmd, self.opid, 1, 1]
            reg.extend(struct.unpack('HH', struct.pack('i', sec)))
            reg.extend(struct.unpack('HH', struct.pack('f', ec)))
            reg.extend(struct.unpack('HH', struct.pack('f', ph)))
        else:
            reg = [cmd, self.opid]

        print(f"{self.get_command_name(cmd)} 명령을 전송합니다. {reg}")
        self.client.write_registers(504, reg, device_id=5)

    def get_status_name(self, stat):
        ctbl = {
            STATCODE.READY: "중지된 상태",
            STATCODE.PREPARING: "준비중",
            STATCODE.SUPPLYING: "관수중",
            STATCODE.FINISHING: "정지중"
        }
        return ctbl.get(stat, "없는 상태")

    def get_remain_time(self, reg1, reg2):
        return struct.unpack('i', struct.pack('HH', reg1, reg2))[0]

    def get_observation(self, reg1, reg2):
        return struct.unpack('f', struct.pack('HH', reg1, reg2))[0]

    def read_status(self, readtime=False):
        reg = self.client.read_holding_registers(401, count=6, device_id=5)
        if not reg.isError():
            if reg.registers[3] == self.opid:
                print(f"OPID {self.opid} 번 명령으로 {self.get_status_name(reg.registers[0])} 입니다.")
                if reg.registers[0] == 1:
                    print(f"양액기 에러입니다. 에러코드는 {reg.registers[2]} 입니다.")
                elif reg.registers[0] != 0 and readtime:
                    print(f"관수구역은 {reg.registers[1]}이고, 남은시간은 {self.get_remain_time(reg.registers[4], reg.registers[5])} 입니다.")
            else:
                print(f"OPID가 매치되지 않습니다. 레지스터값은 {reg.registers[3]}, 기대하고 있는 값은 {self.opid} 입니다.")
        else:
            print("상태 읽기 실패")

    def read_sensors(self):
        # 양액기에 연결된 센서값 읽기
        reg = self.client.read_holding_registers(204, count=3, device_id=5)
        if not reg.isError():
            self.ec = self.get_observation(reg.registers[0], reg.registers[1])
            print(f"EC : {self.ec}", reg.registers)
        else:
            print("EC 센서값 읽기 실패")
            self.ec = 0.0

        reg = self.client.read_holding_registers(213, count=3, device_id=5)
        if not reg.isError():
            self.ph = self.get_observation(reg.registers[0], reg.registers[1])
            print(f"pH : {self.ph}", reg.registers)
        else:
            print("pH 센서값 읽기 실패")
            self.ph = 0.0

        reg = self.client.read_holding_registers(225, count=3, device_id=5)
        if not reg.isError():
            print(f"유량 : {self.get_observation(reg.registers[0], reg.registers[1])}", reg.registers)
        else:
            print("유량 센서값 읽기 실패")

    def run_tests(self):
        self.read_sensors()

        # Initialize
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()

        # 양액 관수 : NUT_WATER
        self.send_command(CMDCODE.NUT_WATER, 30, self.ec, self.ph)
        for _ in range(1, 40):
            self.read_status(True)
            time.sleep(1)

        # 종료 확인
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()
        
        self.client.close()

if __name__ == "__main__":
    with open('conf.json', 'r') as f:
        config = json.load(f)

    tester = NutSupplyTester(config['modbus_ip'], config['modbus_port'])
    tester.run_tests()

