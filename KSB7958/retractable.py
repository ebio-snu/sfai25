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

class RetractableTester:
    def __init__(self, ip, port):
        self.client = ModbusTcpClient(ip, port=port)
        self.client.connect()
        self.devices = ['천창좌', '천창우', '스크린', '보온커튼']
        self.opid = 1
        self.idx = 0

    def get_command_name(self, cmd):
        ctbl = {
            CMDCODE.OFF: "중지",
            CMDCODE.OPEN: "열림",
            CMDCODE.CLOSE: "닫힘",
            CMDCODE.TIMED_OPEN: "시간열림",
            CMDCODE.TIMED_CLOSE: "시간닫힘"
        }
        return ctbl.get(cmd, "없는 명령")

    def send_command(self, cmd, sec=None):
        self.opid += 1
        reg = [cmd, self.opid]

        if sec is not None:
            reg.extend(struct.unpack('HH', struct.pack('i', sec)))

        print(f"{self.get_command_name(cmd)} 명령을 전송합니다. {reg}")
        self.client.write_registers(500 + self.idx, reg, device_id=4)

    def get_status_name(self, stat):
        ctbl = {
            STATCODE.READY: "중지된 상태",
            STATCODE.OPENING: "여는중",
            STATCODE.CLOSING: "닫는중"
        }
        return ctbl.get(stat, "없는 상태")

    def get_remain_time(self, reg1, reg2):
        return struct.unpack('i', struct.pack('HH', reg1, reg2))[0]

    def read_status(self, readtime=False):
        reg = self.client.read_holding_registers(200 + self.idx, count=4, device_id=4)
        if not reg.isError():
            if reg.registers[0] == self.opid:
                print(f"OPID {self.opid} 번 명령으로 {self.get_status_name(reg.registers[1])} 입니다.")
                if reg.registers[1] != 0 and readtime:
                    print(f"작동 남은 시간은 {self.get_remain_time(reg.registers[2], reg.registers[3])} 입니다.")
            else:
                print(f"OPID가 매치되지 않습니다. 레지스터값은 {reg.registers[0]}, 기대하고 있는 값은 {self.opid} 입니다.")
        else:
            print("상태 읽기 실패")

    def run_single_test(self, devidx, devname):
        print(f"\n===== {devname}({devidx}) 장비 테스트 시작 =====\n")
        self.idx = 67 + 4 * devidx

        # Initialize
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()

        # OPEN
        self.send_command(CMDCODE.OPEN)
        for _ in range(1, 10):
            time.sleep(1)
            self.read_status()

        # OFF
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()

        # CLOSE
        self.send_command(CMDCODE.CLOSE)
        for _ in range(1, 10):
            time.sleep(1)
            self.read_status()

        # OFF
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()

        # TIMED OPEN - 10 초 작동
        self.send_command(CMDCODE.TIMED_OPEN, 10)
        for _ in range(1, 15):
            time.sleep(1)
            self.read_status(True)

        # TIMED CLOSE - 10 초 작동
        self.send_command(CMDCODE.TIMED_CLOSE, 10)
        for _ in range(1, 15):
            time.sleep(1)
            self.read_status(True)

        # 종료확인
        self.send_command(CMDCODE.OFF)
        time.sleep(5)
        self.read_status()
        print(f"\n===== {devname}({devidx}) 장비 테스트 종료 =====\n")

    def run_all_tests(self):
        for devidx, devname in enumerate(self.devices):
            self.run_single_test(devidx, devname)
        self.client.close()

if __name__ == "__main__":
    with open('conf.json', 'r') as f:
        config = json.load(f)

    tester = RetractableTester(config['modbus_ip'], config['modbus_port'])
    tester.run_all_tests()


