from colab_ssh.config import config_root_password, install_common_tool
from colab_ssh.ssh import config_ssh_server, parse_public_key
from colab_ssh.tunel import config_argo_tunnel
from colab_ssh.utils import check_gpu_available


def setupSSH(public_key):
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
