# Virtual CAN Hacking Lab

A hands-on, software-only lab for learning automotive network security. No car
and no hardware required: everything runs on a virtual CAN bus on Linux, using
ICSim (the Instrument Cluster Simulator) as a safe target to practice on.

I'm documenting the whole journey here as I build it, from toolset setup to
sniffing and replaying CAN traffic against a simulated dashboard.

## Why this lab

Modern vehicles run on the CAN bus: a network where control units talk with no
built-in authentication. This lab recreates that environment virtually so I can
learn the real attack workflow (sniff, identify, replay, fuzz) safely and
legally, with zero hardware.

## Setup

- OS: Kali Linux (any Linux with SocketCAN works)
- Virtual CAN: SocketCAN `vcan` kernel module
- Tools: `can-utils`, `python-can`
- Target: ICSim (OpenGarages Instrument Cluster Simulator)

Full step-by-step setup lives in [docs/](docs/).

## Roadmap

**Phase 1: Toolset and virtual CAN**
- [ ] Set up the Linux environment
- [ ] Install can-utils and python-can
- [ ] Bring up a virtual CAN interface (vcan0)
- [ ] Send and read the first CAN frames

**Phase 2: CAN fundamentals**
- [ ] Understand CAN frame structure (ID, DLC, data)
- [ ] Sniff, send, and log frames with candump and cansend
- [ ] Write a Python script to send and read frames

**Phase 3: ICSim**
- [ ] Install and run ICSim and controls on vcan0
- [ ] Sniff live traffic and map it
- [ ] Find the frames that control turn signals, speed, and doors
- [ ] Replay captured frames and watch the cluster react

**Phase 4: Analysis and tooling**
- [ ] Use cansniffer to spot changing bytes
- [ ] Build my own replay and simple fuzzing scripts
- [ ] Document the methodology

**Phase 5: UDS basics**
- [ ] Learn UDS (ISO 14229) diagnostic services
- [ ] Explore UDS on the virtual setup

**Phase 6: Toward hardware (future)**
- [ ] Parts list (CANable adapter, instrument cluster)
- [ ] Physical testbed and first real capture

## Repo structure

```
virtual-can-hacking-lab/
├── README.md        overview, roadmap, progress
├── docs/            step-by-step build notes and writeups
├── scripts/         Python and Bash scripts
├── captures/        saved CAN logs
└── notes/           CAN and UDS learning notes
```

## Disclaimer

This project is for education and authorized security research only. Everything
here runs in a virtual environment. Never test on a vehicle you do not own or do
not have explicit permission to test. The author takes no responsibility for
misuse.

## References

- The Car Hacker's Handbook, Craig Smith
- OpenGarages ICSim
- can-utils (Linux SocketCAN tools)
- CSS Electronics CAN bus guide

## About

Built by Dawid Kantowicz as part of my journey into automotive and offensive
security. [LinkedIn](https://www.linkedin.com/in/dawidkantowicz/)
