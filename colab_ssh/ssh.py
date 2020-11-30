import pathlib
import subprocess

from colab_ssh.utils import AptManager


def parse_public_key(public_key):
    if isinstance(public_key, str):
        # URL to text file containt mutilple keys
        if public_key.startswith('http'):
            import urllib.request
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
            else:
                raise ValueError("Key {each_key} are not a public key")
        return public_key


def config_ssh_server(apt_manager, public_key, msg):
    apt_manager = AptManager()
    apt_manager.commit()
    apt_manager.update()
    apt_manager.commit()
    apt_manager.installPkg("openssh-server")
    apt_manager.commit()
    apt_manager.close()

    # Reset host keys
    for i in pathlib.Path("/etc/ssh").glob("ssh_host_*_key"):
        i.unlink()
    subprocess.run(
        ["ssh-keygen", "-A"],
        check=True)

    # Prevent ssh session disconnection.
    with open("/etc/ssh/sshd_config", "a") as f:
        f.write("\n\n# Options added by remocolab\n")
        f.write("ClientAliveInterval 120\n")
        f.write("PasswordAuthentication no\n")
        f.write("Protocol 2\n")
        f.write("PermitRootLogin yes\n")
        f.write("TCPKeepAlive yes\n")
        f.write("X11Forwarding yes\n")
        f.write("X11DisplayOffset 10\n")
        # f.write("AuthorizedKeysFile /.ssh/authorized_keys\n")
        f.write("PubkeyAuthentication yes\n")
        f.write("IgnoreRhosts yes\n")
        f.write("HostbasedAuthentication no\n")
        f.write("PrintLastLog yes\n")
        f.write("AcceptEnv LANG LC_*\n")

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
    for each_key in public_key:
        auth_keys_file.write_text(f"{each_key}\n")
    auth_keys_file.chmod(0o600)

    # Restart SSH service
    subprocess.run(["service", "ssh", "restart"])
    return msg
