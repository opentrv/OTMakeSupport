# OTMakeSupport
Build and CI support for OpenTRV projects.

NOTE: Currently the script will clone the repos/pull the latest commit and attempt to compile V0p2_main. Unfortunately, it does not yet put the libraries in a place the Arduino IDE can see.

## How to use:
- Install Python 3, python3-pip, git and Arduino IDE.
- Run "pip3 install gitpython" to get GitPython.
- Adjust 'REPO_PATH' and 'ARDUINO_BIN' to suit your setup.

Dependencies:
- Only tested on Ubuntu 16.04
- Python 3.x (tested with 3.5.1)
- git
- Arduino IDE 1.6.x (tested with 1.6.8)

Python Dependencies:
- GitPython (https://github.com/gitpython-developers/GitPython)
