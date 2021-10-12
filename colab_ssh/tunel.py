"""Config Argo tunnel for the SSH tunnel"""
import subprocess
import time
import urllib
from typing import Tuple

from colab_ssh.utils import download_file, make_executable


def config_argo_tunnel(msg: str) -> Tuple[str, str, str, str]:
    """
    Config Argo tunnel for the SSH tunnel

    Parameters:
        msg (str): Variable that contain the whole message that will be print out at the end of the setup process

    Return:
        msg (str): The message after added tunnel information and ssh command
        ssh_command (str): The SSH command for Mattermost push notification
        ssh_config (str): The SSH config block for Mattermost push notification
        hostname (str): The hostname of the server, also for Mattermost push notification
    """

    download_file(
        "https://github.com/cloudflare/cloudflared/releases/download/2021.9.2/cloudflared-linux-amd64", "cloudflared")
    make_executable("cloudflared")
    subprocess.run(["./cloudflared", "update"])
    cfd_proc = subprocess.Popen(
        ["./cloudflared", "tunnel", "--url", "ssh://localhost:22",
         "--logfile", "cloudflared.log", "--metrics", "localhost:49589"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    time.sleep(4)
    if cfd_proc.poll() is not None:
        raise RuntimeError("Failed to run cloudflared. Return code:" +
                           str(cfd_proc.returncode) + "\nSee clouldflared.log for more info.")  # pragma: no cover
    hostname = None
    # Sometimes it takes long time to display user host name in cloudflared metrices.
    for _ in range(20):
        with urllib.request.urlopen("http://127.0.0.1:49589/metrics") as response:
            text = str(response.read())
            sub = "\\ncloudflared_tunnel_user_hostnames_counts{userHostname=\"https://"
            begin = text.find(sub)
            if begin == -1:  # pragma: no cover
                time.sleep(10)
                print("Retry reading cloudflared user hostname")
                continue
            end = text.index("\"", begin + len(sub))
            hostname = text[begin + len(sub): end]
            break
    if hostname is None:
        raise RuntimeError(
            "Failed to get user hostname from cloudflared")  # pragma: no cover

    ssh_common_options = "-o UserKnownHostsFile=/dev/null -o VisualHostKey=yes"
    ssh_common_options += " -oProxyCommand=\"cloudflared access ssh --hostname %h\""

    msg += "---\n"
    msg += "Command to connect to the ssh server:\n"
    msg += "✂️"*24 + "\n"
    ssh_command = f"ssh {ssh_common_options} root@{hostname}"
    msg += f"{ssh_command}\n"
    msg += "✂️"*24 + "\n"
    msg += "Or you can use the following configuration in your .ssh/config file:\n"
    msg += "✂️"*24 + "\n"
    ssh_config = f"Host colab\n\tHostName {hostname}\n\tUser root\n\tUserKnownHostsFile /dev/null\n"
    ssh_config += "\tVisualHostKey yes\n\tStrictHostKeyChecking no\n"
    ssh_config += "\tProxyCommand cloudflared access ssh --hostname %h\n"
    msg += ssh_config
    msg += "✂️"*24 + "\n"
    return msg, ssh_command, ssh_config, hostname
