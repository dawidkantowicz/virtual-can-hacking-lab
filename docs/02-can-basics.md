# 02 - CAN Basics: Sniffing, Sending, and Logging

Now that vcan0 is live, this phase covers the core can-utils workflow:
generating traffic, sniffing it, logging it, and spotting changing data.
This is the foundation of every CAN attack: you have to read the bus before
you can influence it.

## Goal

- Generate CAN traffic on vcan0
- Sniff and log frames
- Watch which bytes change with cansniffer
- Read frames with a Python script (python-can)

## Steps

### 1. Generate traffic

With `vcan0` up, I generated random CAN traffic to simulate a busy bus.

Terminal 1 (listen):
```bash
candump vcan0
```

Terminal 2 (generate random frames):
```bash
cangen vcan0 -v
```

Sample of what appeared on the bus:
```
vcan0  3AB   [8]  40 07 85 6B 4B A0 71 2B
vcan0  3AE   [8]  C5 1A AA 11 E2 22 AE 2E
vcan0  0A3   [4]  31 2A DA 2A
vcan0  65B   [8]  31 E0 0E 48 F0 85 45 33
```

**Reading a frame:** `interface  ID  [DLC]  data bytes`
- **ID** (hex) identifies the message / sender and sets bus priority.
- **DLC** is how many data bytes follow (0–8 for classic CAN).
- **Data** is the payload (in a real car: speed, RPM, button states, etc.).

Note: there is no sender field and no authentication in a CAN frame — any node
can send any ID. This is the core weakness that makes CAN attacks possible.

### 2. Sniff and log

To analyze or replay traffic later, capture it to a file with `candump -l`:

```bash
candump -l vcan0      # writes to candump-<timestamp>.log
cangen vcan0 -v       # (second terminal) generate traffic to capture
```

Check the saved log:
```bash
ls -l candump-*.log
cat candump-*.log | head -5
```

Sample log contents:
```
(1789486722.921502) vcan0 680#5198F121B799BC18
(1789486723.121910) vcan0 49B#16E4513296545948
(1789486723.322309) vcan0 561#FF51973A505F2624
(1789486723.522821) vcan0 2D8#0E
(1789486723.723636) vcan0 065#
```

**Log format:** `(timestamp) interface ID#data`
- The **timestamp** preserves exact frame timing — essential for realistic replay.
- Frames use compact `ID#DATA` notation (e.g. `2D8#0E` = ID 2D8, one data byte).
- A frame can have 0 bytes (`065#`) — valid in CAN.

This log file is now a recording of the bus that can be replayed back.

### 3. Replay captured traffic

The captured log can be replayed straight back onto the bus with `canplayer`:

```bash
candump vcan0                    # terminal 1: watch the replay arrive
canplayer -I candump-<file>.log  # terminal 2: replay the log
```

Terminal 1 showed the exact frames from the log replaying back, with their
original IDs, lengths, and data; the capture reproduced faithfully.

**Why this matters:** capture + replay is the foundational CAN attack. Sniff the
bus while an action happens (e.g. unlocking a door), isolate the frame(s) that
action produced, then replay them, and the ECU performs the action again,
because CAN frames carry no authentication. The receiver cannot tell a replayed
frame from a genuine one.

### 4. Read frames with Python
_Script and notes go here._

## What I learned
_Real notes and any hiccups go here._
