"""Just look at the name, it's main"""
import time

from colab_ssh.config import config_root_password, install_common_tool
from colab_ssh.notification import send_notification_to_microsoft_teams
from colab_ssh.ssh import config_ssh_server, parse_public_key
from colab_ssh.tunel import config_argo_tunnel
from colab_ssh.utils import check_gpu_available, get_instance_info


def setup_ssh(public_key, teams_webhook_address: str = None):
    """
    Setup an SSH tunel to the current Colab notebook instance with ssh public key authentication

    Parameters:
        public_key:
            - (str): The public key that will be able to authenticate the SSH connection
            - (List[str]): A list of public keys that will be able to authenticate the SSH connection
            - (str): Link to a text file (authorized_keys) that cotains all the public keys that will be
            able to authenticate the SSH connection
        webhook_address:
            - (str): The webhook address for microsoft teams for push notification

    After about 2 minutes of running, the bash command to initialize the SSH connection will be print out
    """
    public_key = parse_public_key(public_key)

    if not check_gpu_available():
        return  # pragma: no cover

    # Config password for root user
    msg = ""
    msg = config_root_password(msg)

    # Config ssh server
    msg = config_ssh_server(public_key, msg)

    # Config other common tool and library
    install_common_tool()

    # Config Argo Tunnel
    msg, ssh_command, hostname = config_argo_tunnel(msg)

    # Send notification to Microsoft Teams
    if teams_webhook_address is not None:
        spec = get_instance_info()
        spec['ssh_command'] = ssh_command
        spec['hostname'] = hostname
        send_notification_to_microsoft_teams(teams_webhook_address, spec)

    print(msg)


def loop_forever():  # pragma: no cover
    """
    Utility function to keep the colab notebook from disconnecting the kernel.
    """
    while True:
        time.sleep(15)
