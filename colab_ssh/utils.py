import apt
from colab_ssh.progress_bar import NoteProgress
import urllib.request
import shutil
import subprocess
import IPython.utils.io
from IPython.core.getipython import get_ipython

def download_file(url, path):
    try:
        with urllib.request.urlopen(url) as response:
            with open(path, 'wb') as outfile:
                shutil.copyfileobj(response, outfile)
    except:
        print("Failed to download ", url)
        raise


def get_gpu_name():
    r = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                       stdout=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def check_gpu_available():
    gpu_name = get_gpu_name()
    if gpu_name == None:
        print("This is not a runtime with GPU")
    elif gpu_name == "Tesla K80":
        print("Warning! GPU of your assigned virtual machine is Tesla K80.")
        print("You might get better GPU by reseting the runtime.")
    else:
        print(f"This runtime was assigned to GPU: {gpu_name}")
        return True
    return IPython.utils.io.ask_yes_no("Do you want to continue? [y/n]")


def run_command(setup_script):
    for command in (setup_script.split("\n")):
        command = command.strip()
        get_ipython().system_raw(command)


class AptManager:
    def __init__(self):
        self._progress = NoteProgress()
        self._cache = apt.Cache(self._progress)

    def close(self):
        self._cache.close()
        self._cache = None
        self._progress.close()
        self._progress = None

    def update(self):
        print("Updating apt package")
        self._cache.update()
        self._cache.open(None)

    def upgrade(self):
        self._cache.upgrade()

    def update_upgrade(self):
        self._cache.update()
        self._cache.open(None)
        self._cache.upgrade()

    def commit(self):
        self._cache.commit(self._progress, self._progress)
        self._cache.clear()

    def installPkg(self, *args):
        for name in args:
            pkg = self._cache[name]
            if pkg.is_installed:
                print(f"{name} is already installed")
            else:
                print(f"Install {name}")
                pkg.mark_install()

    def installDebPackage(self, name):
        apt.debfile.DebPackage(name, self._cache).install()

    def deleteInstalledPkg(self, *args):
        for pkg in self._cache:
            if pkg.is_installed:
                for name in args:
                    if pkg.name.startswith(name):
                        #print(f"Delete {pkg.name}")
                        pkg.mark_delete()
