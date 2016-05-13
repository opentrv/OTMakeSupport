#! python3

from git import Repo
import os
import subprocess

# Adjust these for your setup.
REPO_BRANCH = 'master'  # Branch being tested
REPO_PATH = ''  # Location of folder to clone git repos into. Note that python doesn't seem to recognise '~/'
ARDUINO_BIN = ''  # Command to run Arduino IDE (path to binary or 'arduino' if you installed your IDE.
ARDUINO_FLAGS = '--verify'  # Flags to pass the IDE. See https://github.com/arduino/Arduino/blob/ide-1.5.x/build/shared/manpage.adoc
# No need to change these
REPO_LOCALS = {'opentrv': 'opentrv', 'otradiolink': 'otradiolink', 'otaesgcm': 'otaesgcm'}  # Names for local repos
SKETCH_PATH = 'opentrv/Arduino/V0p2_Main/V0p2_Main.ino'  # Path V0p2_main.ino relative to REPO_PATH
REPO_REMOTES = {'opentrv': 'https://github.com/DamonHD/OpenTRV',
                'otradiolink': 'https://github.com/opentrv/OTRadioLink',
                'otaesgcm': 'https://github.com/opentrv/OTAESGCM'}  # Links to Git repos.

# global variables.
join = os.path.join  # shortcut function
my_repos = None  # global declaration

try:
    # Try updating local repos.
    print("Updating repos")
    my_repos = {'opentrv': Repo(join(REPO_PATH, REPO_LOCALS['opentrv'])),
                'otradiolink': Repo(join(REPO_PATH, REPO_LOCALS['otradiolink'])),
                'otaesgcm': Repo(join(REPO_PATH, REPO_LOCALS['otaesgcm']))}  # This adds existing repos to my_repos

    def update_repo(repo):
        """Makes sure master is checked out and then does a git pull.
        :param repo: git repo to update
        :return: None
        """
        print('updating ' + repo.__repr__())
        repo.heads.master.checkout()
        repo.remotes.origin.pull()
    {k: update_repo(repo) for k, repo in my_repos.items()}  # iterate through my_repos, updating them all.
except:
    # Attempt to clone REPO_REMOTES. TODO probably need some better checks.
    print("Local repos not found. Clone to " + REPO_PATH + "?")
    response = input("[Y/n]")
    print("downloading...")
    if (response == 'Y') or (response == 'y') or (response == '\n'):
        my_repos = {'opentrv': Repo.clone_from(REPO_REMOTES['opentrv'], join(REPO_PATH, REPO_LOCALS['opentrv']),
                                               branch=REPO_BRANCH),
                    'otradiolink': Repo.clone_from(REPO_REMOTES['otradiolink'], join(REPO_PATH, REPO_LOCALS['otradiolink']),
                                                   branch=REPO_BRANCH),
                    'otaesgcm': Repo.clone_from(REPO_REMOTES['otaesgcm'], join(REPO_PATH, REPO_LOCALS['otaesgcm']),
                                                branch=REPO_BRANCH)}  # Clone repos into REPO_PATH


# Try compiling with the arduino IDE. 'stdout=subprocess.PIPE' pipes the output to the shell.
subprocess.run([ARDUINO_BIN, ARDUINO_FLAGS, join(REPO_PATH, SKETCH_PATH)], stdout=subprocess.PIPE)
