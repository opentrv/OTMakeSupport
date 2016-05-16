# OTMakeSupport
Build and CI support for OpenTRV projects.

NOTE: Currently the script will clone the repos/pull the latest commit and attempt to compile V0p2_main. Unfortunately, it does not yet put the libraries in a place the Arduino IDE can see.

## How to use:
- Install Python 3, python3-pip, git and Arduino IDE.
- Run "pip3 install gitpython" to get GitPython.
- Adjust 'REPO_PATH' and 'ARDUINO_BIN' to suit your setup.
- Target board can be chosen by setting BUILD_TARGET. Default is the OpenTRV V0p2. See https://github.com/arduino/Arduino/blob/ide-1.5.x/build/shared/manpage.adoc
- Run the script. If the repos are not already there, it will prompt to clone them to REPO_PATH.
- The script will exit with the return code the arduino environment exits with.
    0. Success
    1. Build failed or upload failed
    2. Sketch not found
    3. Invalid (argument for) commandline option
    4. Preference passed to --get-pref does not exist


## Dependencies:
- Only tested on Ubuntu 16.04
- Python 3.x (tested with 3.5.1)
- git
- Arduino IDE 1.6.x (tested with 1.6.8)

## Python Dependencies:
- GitPython (https://github.com/gitpython-developers/GitPython)
