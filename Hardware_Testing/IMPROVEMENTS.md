# Stuff to remember
- Manifest of what should be supplied and what user will need.
    - e.g. monitor, mains sockets etc.
- Troubleshooting for getting everything working. (e.g. make sure sd card inserted)
- Phone number for support
- Schematic diagram of interface hardware.
- Use FR4 for circuits.
- ESD measures.
- Supply spares of frequently inserted cables.
- Supply some guaranteed working boards for checking setup before running a batch.
- Test script should indicate what firmware version it needs.
- Firmware should print what version it is to serial.
- What success and failure look like in the manual.

# Possible improvements to the test process
## Hardware
- Make sure the polarity of any connectors can be clearly identified, using conventions if possible on wiring.
- Use polarised connectors if possible - Not possible currently but really really want this!
- Tie down all cables on hardware.
- Cases on hardware.
- Sleeves/hot glue to make cables robust.
- Protection for Pi (optoisolation, run device of separate PSU).

## Firmware + test script
- Serial number for all boards.
- How long does a successful test take?
- How do label failures?
