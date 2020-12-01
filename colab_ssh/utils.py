"""Contain utils function"""

import os
import multiprocessing
import shutil
import subprocess
import urllib.request
from typing import Dict

import IPython.utils.io
from IPython.core.getipython import get_ipython
from psutil import virtual_memory
import apt

from colab_ssh.progress_bar import NoteProgress


def download_file(url: str, path: str):
    """
    Download a file from a given URL

    Parameters:
        - url (str): Url to the file to be downloaded
        - path (str): Path to save the file
    """
    try:
        with urllib.request.urlopen(url) as response:
            with open(path, 'wb') as outfile:
                shutil.copyfileobj(response, outfile)
    except Exception:  # pragma: no cover
        print("Failed to download ", url)
        raise


def get_gpu_name():
    """
    Get current GPU name
    """
    try:
        process = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                                stdout=subprocess.PIPE, universal_newlines=True, check=False)
        if process.returncode != 0:  # pragma: no cover
            return None
        return process.stdout.strip()  # pragma: no cover
    except FileNotFoundError:
        return None

def check_gpu_available():
    """
    Check if any GPU is available
    """
    gpu_name = get_gpu_name()
    if gpu_name is None:
        print("This is not a runtime with GPU")
    elif gpu_name == "Tesla K80":  # pragma: no cover
        print("Warning! GPU of your assigned virtual machine is Tesla K80.")
        print("You might get better GPU by reseting the runtime.")
    else:  # pragma: no cover
        print(f"This runtime was assigned to GPU: {gpu_name}")
        return True
    if os.environ.get("IS_TESTING_CI") is not None:
        print("Testing on non GPU machine detected")
        return True
    else:
        return IPython.utils.io.ask_yes_no("Do you want to continue? [y/n]")  # pragma: no cover


def run_command(setup_script: str):
    """
    Run a mutilple line of bash command.

    Parameters:
        - setup_script (str): The multi line string of bash to execute
    """
    for command in setup_script.split("\n"):
        command = command.strip()
        if os.environ.get("IS_TESTING_CI") is None:
            get_ipython().system_raw(command)  # pragma: no cover


def get_instance_info() -> Dict:
    """
    Get current instance information

    Return: A dictionary of instance
        {
            'cpu': (str) Number of CPUs cores,
            'ram': (str) RAM size in GB,
            'gpu': (str) GPU name with VRAM size in GB
        }
    """
    try:
        gpu_info = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, check=False)
        gpu_info = gpu_info.stdout.decode("utf-8")  # pragma: no cover
    except FileNotFoundError:
        gpu_info = 'failed'
    if 'failed' in gpu_info:
        gpu_type = 'N/A'
        gpu_vram_gb = 0
    else:  # pragma: no cover
        raw_gpu_info = gpu_info.split('\n')
        gpu_info = [each for each in raw_gpu_info if '0  Tesla' in each][0]
        gpu_type = None
        possible_gpu_type = ['P100', 'K80', 'T4', 'V100']
        for each in possible_gpu_type:
            if each in gpu_info:
                gpu_type = 'NVIDIA Tesla {}'.format(each)
                break
        gpu_info = [each for each in raw_gpu_info if 'MiB' in each]
        gpu_vram_gb = int(gpu_info[0].split(
            '|')[-3].split('/')[-1].strip().replace('MiB', ''))/1024
        if gpu_type is not None:
            gpu_type = "{} - {:.2f} GB".format(gpu_type, gpu_vram_gb)
    total_ram = virtual_memory().total / 1e9
    return {
        'cpu':  f"{multiprocessing.cpu_count()} cores",
        'gpu': gpu_type,
        'ram': "{:.2f} GB".format(total_ram),
    }


class AptManager:
    """
    Apt manager for better apt packages management
    """

    def __init__(self):
        self._progress = NoteProgress()
        self._cache = apt.Cache(self._progress)

    def close(self):
        """
        Delete the manager
        """
        self._cache.close()
        self._cache = None
        self._progress.close()
        self._progress = None

    def update(self):
        """
        Similar to `sudo apt update`
        """
        print("Updating apt package")
        self._cache.update()
        self._cache.open(None)

    def upgrade(self):
        """
        Similar to `sudo apt upgrade`
        """
        self._cache.upgrade()  # pragma: no cover

    def commit(self):
        """
        Lock cache and add new step to the progress bar
        """
        self._cache.commit(self._progress, self._progress)
        self._cache.clear()

    def install_pkg(self, *args):
        """
        Install packages, similar to `sudo apt install xxx`
        """
        for name in args:
            pkg = self._cache[name]
            if pkg.is_installed:
                print(f"{name} is already installed")
            else:
                print(f"Install {name}")
                pkg.mark_install()
