#!/usr/bin/env python3
"""Read and print CAN frames from vcan0 using python-can."""
import can

def main():
    # connect to the virtual CAN bus
    bus = can.interface.Bus(channel="vcan0", interface="socketcan")
    print("Listening on vcan0 ... (Ctrl+C to stop)\n")
    try:
        for msg in bus:
            data = " ".join(f"{b:02X}" for b in msg.data)
            print(f"ID: {msg.arbitration_id:03X}  [{msg.dlc}]  {data}")
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
