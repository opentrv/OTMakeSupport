#! python3

from git import Repo
import os

join = os.path.join

# Path names
REPO_REMOTES = {'opentrv': 'https://github.com/DamonHD/OpenTRV',
                'otradiolink' : 'https://github.com/opentrv/OTRadioLink',
                'otaesgcm' : 'https://github.com/opentrv/OTAESGCM'}
REPO_BRANCH = 'master'
REPO_PATH = '/home/denzo/OpenTRV/OTMakeSupport_test'
REPO_LOCALS = {'opentrv': 'opentrv', 'otradiolink': 'otradiolink', 'otaesgcm': 'otaesgcm'}
ARDUINO_BIN = '/home/denzo/OpenTRV/Arduino'

my_repos = None

try:
    #
    print("Updating repos")
    my_repos = {'opentrv': Repo(join(REPO_PATH, REPO_LOCALS['opentrv'])),
                'otradiolink': Repo(join(REPO_PATH, REPO_LOCALS['otradiolink'])),
                'otaesgcm': Repo(join(REPO_PATH, REPO_LOCALS['otaesgcm']))}

    def update_repo(repo):
        print('updating ' + repo.__repr__())
        repo.heads.master.checkout()
        repo.remotes.origin.pull()
    {k: update_repo(repo) for k, repo in my_repos.items()}
except:
    # Attempt to clone REPO_REMOTES
    print("Local repos not found. Clone to " + REPO_PATH + "?")
    response = input("[Y/n]")
    print("downloading...")
    if (response == 'Y') or (response == 'y') or (response == '\n'):
        my_repos = {'opentrv': Repo.clone_from(REPO_REMOTES['opentrv'], join(REPO_PATH, REPO_LOCALS['opentrv']), branch=REPO_BRANCH),
                    'otradiolink': Repo.clone_from(REPO_REMOTES['otradiolink'], join(REPO_PATH, REPO_LOCALS['otradiolink']), branch=REPO_BRANCH),
                    'otaesgcm': Repo.clone_from(REPO_REMOTES['otaesgcm'], join(REPO_PATH, REPO_LOCALS['otaesgcm']), branch=REPO_BRANCH)}

print("success")
