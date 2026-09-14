# 01 - Setup: Toolset and Virtual CAN

This is the starting point of the lab: getting the environment ready and
bringing up a virtual CAN bus, with no hardware required.

## Goal

- Install the CAN tooling
- Create a virtual CAN interface (vcan0)
- Send and read the first CAN frame

## Environment

- OS: Kali Linux
- (to be filled in as I go)

## Steps

### 1. Install the tools
On Kali, checked whether the CAN tooling was already present:

```bash
which candump cansend
```

Both were already installed (Kali ships with `can-utils` in many builds), so no
install was needed. To install on a system that doesn't have it:

```bash
sudo apt update
sudo apt install can-utils -y
```

Also installed the Python CAN library:
```bash
pip install python-can
```

### 2. Load the virtual CAN module
Virtual CAN is provided by the `vcan` kernel module. Load it with:

```bash
sudo modprobe vcan
```

This adds virtual CAN support to the kernel so we can create a fake CAN
interface with no hardware.

### 3. Bring up vcan0
Create a virtual CAN interface called `vcan0` and bring it online:

```bash
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Confirm it exists and is up:
```bash
ip link show vcan0
```
Output showed `vcan0` in state `UNKNOWN` (normal for virtual CAN) - the bus is
now live.

### 4. First frame test
Open two terminals. In the first, listen on the bus:
```bash
candump vcan0
```

In the second, send a test frame:
```bash
cansend vcan0 123#DEADBEEF
```

The frame appeared in the first terminal - virtual CAN is working end to end.

## What I learned
- Kali already had can-utils installed; worth checking your environment before
  installing.
- Hit the "externally-managed-environment" error with pip, solved it by using a
  Python virtual environment.
- Virtual CAN (vcan) lets you build a working CAN bus with zero hardware.
