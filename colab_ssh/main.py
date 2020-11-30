import time

from colab_ssh.config import config_root_password, install_common_tool
from colab_ssh.ssh import config_ssh_server, parse_public_key
from colab_ssh.tunel import config_argo_tunnel
from colab_ssh.utils import check_gpu_available


def setupSSH(public_key):
    """
    Setup an SSH tunel to the current Colab notebook instance with ssh public key authentication

    Arguments:
        public_key:
            - (str): The public key that will be able to authenticate the SSH connection
            - (List[str]): A list of public keys that will be able to authenticate the SSH connection
            - (str): Link to a text file (authorized_keys) that cotains all the public keys that will be able to authenticate the SSH connection
    
    After about 2 minutes of running, the bash command to initialize the SSH connection will be print out
    """
    public_key = parse_public_key(public_key)

    if not check_gpu_available():
        return False

    # Config password for root user
    msg = ""
    msg = config_root_password(msg)

    # Config ssh server
    msg = config_ssh_server(public_key, msg)

    # Config other common tool and library
    msg = install_common_tool(msg)

    # Config Argo Tunnel
    msg = config_argo_tunnel(msg)
    print(msg)


def loop_forever():
    """
    Utility function to keep the colab notebook from disconnecting the kernel.
    """
    while True:
        time.sleep(15)