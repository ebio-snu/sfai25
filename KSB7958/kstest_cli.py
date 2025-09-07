#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 tombraid@snu.ac.kr
# All right reserved.
#
import argparse
import json
import sys
from switch import SwitchTester
from retractable import RetractableTester
from nutsupply import NutSupplyTester

def run_tests(tester, device_index=None):
    if hasattr(tester, 'devices') and device_index is not None:
        if 0 <= device_index < len(tester.devices):
            dev_name = tester.devices[device_index]
            tester.run_single_test(device_index, dev_name)
        else:
            print(f"Error: Device index {device_index} is out of range.")
            print(f"Available device indices: 0 to {len(tester.devices) - 1}")
    elif hasattr(tester, 'run_all_tests'):
        tester.run_all_tests()
    elif hasattr(tester, 'run_tests'): # For NutSupplyTester
        tester.run_tests()

def interactive_mode(ip, port):
    print("KSTEST Interactive Mode")
    print("-----------------------")
    
    while True:
        # 1. Select device type
        print("\nSelect device type:")
        device_types = ['switch', 'retractable', 'nutsupply']
        for i, dtype in enumerate(device_types):
            print(f"  {i+1}. {dtype}")
        
        choice = -1
        while choice not in range(1, len(device_types) + 1):
            try:
                raw_choice = input(f"Enter number (1-{len(device_types)}): ")
                choice = int(raw_choice)
            except ValueError:
                print("Invalid input. Please enter a number.")

        selected_type = device_types[choice - 1]

        # 2. Select specific device or all
        if selected_type == 'switch':
            tester = SwitchTester(ip, port)
            prompt_for_device_selection(tester)
        elif selected_type == 'retractable':
            tester = RetractableTester(ip, port)
            prompt_for_device_selection(tester)
        elif selected_type == 'nutsupply':
            print("\nRunning nutsupply tests...")
            tester = NutSupplyTester(ip, port)
            tester.run_tests()

        # 3. Ask to continue
        while True:
            another = input("\nDo you want to perform another test? (y/n): ").lower()
            if another in ['y', 'yes', 'n', 'no']:
                break
        if another in ['n', 'no']:
            print("Exiting interactive mode. Goodbye!")
            break

def prompt_for_device_selection(tester):
    print(f"\nSelect a device to test for '{tester.__class__.__name__}':")
    for i, name in enumerate(tester.devices):
        print(f"  {i}. {name}")
    print("  all - Test all devices")

    while True:
        raw_choice = input(f"Enter device index (0-{len(tester.devices)-1}) or 'all': ")
        if raw_choice.lower() == 'all':
            run_tests(tester)
            return
        try:
            choice = int(raw_choice)
            if 0 <= choice < len(tester.devices):
                run_tests(tester, choice)
                return
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a number or 'all'.")

def main():
    with open('conf.json', 'r') as f:
        config = json.load(f)
    ip = config['modbus_ip']
    port = config['modbus_port']

    if len(sys.argv) == 1:
        interactive_mode(ip, port)
    else:
        parser = argparse.ArgumentParser(description="KSTEST Command Line Interface")
        parser.add_argument('type', choices=['switch', 'retractable', 'nutsupply'], help='Type of device to test')
        parser.add_argument('--device', type=int, help='The index of the device to test. If not provided, all devices of the type will be tested.')
        args = parser.parse_args()

        if args.type == 'switch':
            tester = SwitchTester(ip, port)
            run_tests(tester, args.device)
        elif args.type == 'retractable':
            tester = RetractableTester(ip, port)
            run_tests(tester, args.device)
        elif args.type == 'nutsupply':
            if args.device is not None:
                print("Error: --device option is not applicable for nutsupply.")
            else:
                tester = NutSupplyTester(ip, port)
                tester.run_tests()

if __name__ == "__main__":
    main()
