# 04 - UDS: Talking to an ECU and Reading Its Responses

Phase 3 was the network layer - raw CAN frames, broadcast and replayed. UDS
(Unified Diagnostic Services, ISO 14229) is the layer above: a request/response
protocol used to interrogate and command a specific ECU. Using OpenGarages'
UDSim (a graphical UDS simulator built to pair with ICSim), I sent UDS requests
to a simulated ECU and learned to read both its positive and negative responses.

## What UDS is
- Request/response, not broadcast: you address a specific ECU and it answers.
- Positive response = request service ID + 0x40 (so 0x10 -> 0x50).
- Negative response = 0x7F, followed by the service and an NRC (Negative
  Response Code) explaining the refusal.
- Key services: 0x10 DiagnosticSessionControl, 0x22 ReadDataByIdentifier,
  0x27 SecurityAccess, 0x2E WriteDataByIdentifier, 0x11 ECUReset.

## Setup
- UDSim built from source, running on vcan0 with an example config (ECU at 7E0,
  responses on 7E8).
- Simulation mode, with "Fake Responses" enabled so the ECU attempts a reply to
  services it hasn't explicitly learned.
- Tools: can-utils (cansend, candump).

## The conversation
Requests sent to 7E0, responses observed on 7E8:

```
7E0  02 10 03              DiagnosticSessionControl (extended session)
7E8  06 50 03 00 96 17 70  POSITIVE (0x50 = 0x10 + 0x40) - session changed
7E0  03 22 F1 90           ReadDataByIdentifier (DID F190 - VIN)
7E8  03 7F 22 31           NEGATIVE - service 0x22, NRC 0x31 (requestOutOfRange)
7E0  02 27 01              SecurityAccess (request seed)
7E8  03 7F 27 35           NEGATIVE - service 0x27, NRC 0x35 (invalidKey)
```

## Reading the responses
- **0x50** confirmed the positive-response rule (SID + 0x40). The ECU accepted
  the session change.
- **0x7F ... 0x31** on ReadDataByIdentifier means the identifier isn't available
  (no VIN stored in this config).
- **0x7F ... 0x35** on SecurityAccess shows the ECU is reachable and processing
  the seed-request flow, but gating access behind its key logic.

## Why the negatives matter
An ECU's refusals leak information. By sending services and reading the NRCs,
you map the attack surface before exploiting anything: which services exist,
which need a session first, which are gated behind SecurityAccess, and which
data identifiers are valid. SecurityAccess (0x27) is the protected gate - on a
real ECU with weak seed/key logic, this is exactly the door a pentester would
then try to pick.

## What I learned
- The positive/negative response format (0x40 offset; 0x7F + NRC) is the core
  grammar of UDS - once you can read it, every response tells you something.
- Negative responses are a feature, not a failure: NRCs are a map of the ECU.
- Simulation mode only answers what it has learned or been configured for; the
  next step is Learning mode against realistic traffic for a fuller ECU.
- Small hiccups: cansend needs full-byte data (even digit count)

<img width="717" height="481" alt="image" src="https://github.com/user-attachments/assets/3435e856-d63c-4ccd-80db-3c8360dabdc1" />
<img width="1273" height="1255" alt="image" src="https://github.com/user-attachments/assets/e8ade066-c816-4fdc-b61f-6f8b6ed8d327" />

