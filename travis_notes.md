## Before install steps:
1. Setup dummy X server for Arduino IDE.
2. Download Arduino 1.6.8, OTRadioLink and OTAESGCM.
3. Extract them all.
4. Move Arduino IDE to /usr/local/share/ and add to path.

## Install steps:
1. ?? (ln -s $PWD /usr/local/share/arduino/libraries/)
2. Install OpenTRV board.
    - This will require editing preferences.txt first.
3. Install OpenTRV libs.
    - Will have to manually install.

## Script:
- Verify V0p2_main.ino compiles.

## Notification:
- Send a notification email on success and failure.
