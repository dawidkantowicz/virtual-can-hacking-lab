# 03 - ICSim: Finding and Replaying the Turn Signal

Using OpenGarages' ICSim (a simulated instrument cluster) as a target, I
practiced the core CAN attack workflow on realistic traffic: sniff, isolate the
frame behind an action, decode it, and replay it.

## Setup
- ICSim (icsim + controls) running on vcan0
- Tools: candump, cansniffer, cansend

## Finding the frame
- candump alone was unreadable - a flood of frames.
- cansniffer -c grouped traffic by ID and highlighted changes.
- Filtered out the noise (`-000000` to hide all, `+188` to show one ID).
- Toggling the turn signal changed only ID **188**.

## Decoding
- 188 signal OFF: 00 00 00 00
- 188 LEFT on:    01 00 00 00
- 188 RIGHT on:   02 00 00 00
- Byte 0 is the turn-signal state (01 = left, 02 = right).

## The replay attack
```bash
cansend vcan0 188#01000000   # left signal
cansend vcan0 188#02000000   # right signal
```
Injecting the frame flashed the blinker with no input from the controls window -
the cluster obeyed a frame I crafted, because CAN has no authentication.

## What I learned

- **A live CAN bus is overwhelming at first - filtering is everything.** With
  every ECU talking at once, `candump` was just a wall of scrolling frames. The
  turn signal was impossible to spot in the noise. `cansniffer` with ID grouping
  and change-highlighting is what made it workable, and muting all IDs
  (`-000000`) then showing one (`+188`) turned "needle in a haystack" into an
  obvious before/after test.

- **Don't trust the first flicker - confirm it.** My first candidate looked like
  ID 40C, but when I isolated it and toggled the signal, it wasn't the one. I had
  to repeat the process a few times before landing on the real frame, 188. Lesson:
  correlate the action with the change deliberately, and verify - the first thing
  that catches your eye isn't always the answer.

- **Reading the bytes beats reading the colors.** Instead of relying on what
  "lit up," watching the actual data values change (00 -> 01 -> 02) as I toggled
  the signal gave a clear, unambiguous decode: byte 0 holds the state.

- **The replay worked because CAN has no authentication.** Injecting my own 188
  frame flashed the blinker with the controls window doing nothing - the cluster
  can't tell a crafted frame from a genuine one. Seeing that first-hand, after
  reading about it, made the core weakness of CAN finally click.

- Honestly, this was the moment the whole thing became real for me - going from
  "it's just a mess" to finding and controlling a specific function on the bus in
  a matter of minutes. This is exactly the kind of work I want to do.
