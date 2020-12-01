"""Config SSHD server"""
import pathlib
import subprocess
import urllib.request
from typing import List

from colab_ssh.utils import AptManager


def parse_public_key(public_key) -> List[str]:
    """
    Parse input public key to a list of public SSH key with basic checking

    Parameters:
        public_key:
            - (str): The public key that will be able to authenticate the SSH connection
            - (List[str]): A list of public keys that will be able to authenticate the SSH connection
            - (str): Link to a text file (authorized_keys) that cotains all the public keys that will be
            able to authenticate the SSH connection

    Return:
        public_key:
            - (List[str]): A list of public keys that will be able to authenticate the SSH connection
    """
    if isinstance(public_key, str):
        # URL to text file containt mutilple keys
        if public_key.startswith('http'):
            public_key = [line.decode('utf-8')
                          for line in urllib.request.urlopen(public_key)]
        # Single key
        else:
            public_key = [public_key]
    # List of public keys in string format
    if isinstance(public_key, list):
        for each_key in public_key:
            each_key = each_key.strip()
            if isinstance(each_key, str) and each_key.startswith('ssh-'):
                continue
            raise ValueError("Key {each_key} are not a public key")
        return public_key
    return []

def config_ssh_server(public_key: List[str], msg: str):
    """
    Install SSH server, config it and set the appropriate public_key for authentication

    Parameters:
        public_key (List[str]): A list of string of parsed public keys
        msg (str):  Variable that contain the whole message that will be print out at the end of the setup process
    """
    apt_manager = AptManager()
    apt_manager.commit()
    apt_manager.update()
    apt_manager.commit()
    apt_manager.install_pkg("openssh-server")
    apt_manager.commit()
    apt_manager.close()

    # Reset host keys
    for i in pathlib.Path("/etc/ssh").glob("ssh_host_*_key"):
        i.unlink()
    subprocess.run(
        ["ssh-keygen", "-A"],
        check=True)

    # Prevent ssh session disconnection.
    with open("/etc/ssh/sshd_config", "a") as file:
        file.write("\n\n# Options added by remocolab\n")
        file.write("ClientAliveInterval 120\n")
        file.write("PasswordAuthentication no\n")
        file.write("Protocol 2\n")
        file.write("PermitRootLogin yes\n")
        file.write("TCPKeepAlive yes\n")
        file.write("X11Forwarding yes\n")
        file.write("X11DisplayOffset 10\n")
        file.write("PubkeyAuthentication yes\n")
        file.write("IgnoreRhosts yes\n")
        file.write("HostbasedAuthentication no\n")
        file.write("PrintLastLog yes\n")
        file.write("AcceptEnv LANG LC_*\n")

    msg += "ECDSA key fingerprint of host:\n"
    ret = subprocess.run(
        ["ssh-keygen", "-lvf", "/etc/ssh/ssh_host_ecdsa_key.pub"],
        stdout=subprocess.PIPE,
        check=True,
        universal_newlines=True)
    msg += ret.stdout + "\n"

    # Setup public_key
    home_dir = pathlib.Path("/root")
    ssh_dir = home_dir / ".ssh"
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    auth_keys_file = ssh_dir / "authorized_keys"
    auth_keys_file.write_text("\n".join(public_key))
    auth_keys_file.chmod(0o600)

    # Restart SSH service
    subprocess.run(["service", "ssh", "restart"], check=False)
    return msg
