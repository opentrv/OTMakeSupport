# Aim
Test the current version of our repos compiles (testing different build configs etc. don't matter for now).

# What it needs to do
## Setup
- Download and setup Arduino IDE
- Install the opentrv v0p2 board
    - Edit preferences.txt to add the v0p2 board (need to add the link in the readme for [OpenTRV-Config/Arduino](https://github.com/opentrv/OpenTRV-Config/tree/master/Arduino) repo)
    - Run 'arduino --install-board "opentrv:avr:opentrv_v0p2"' to actually install the board.
- Download and setup OTRadioLink and OTAESGCM (Does the OpenTRV repo need to be downloaded as well?).

## Test
- Verify V0p2_main.ino compiles.
    - 'arduino --verify --board opentrv:avr:opentrv_v0p2 /path-to-V0p2_main.ino'
