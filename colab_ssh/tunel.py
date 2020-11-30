import shutil
import subprocess
import time
import urllib

from colab_ssh.utils import download_file


def config_argo_tunnel(msg):
    download_file(
        "https://bin.equinox.io/c/VdrWdbjqyF/cloudflared-stable-linux-amd64.tgz", "cloudflared.tgz")
    shutil.unpack_archive("cloudflared.tgz")
    cfd_proc = subprocess.Popen(
        ["./cloudflared", "tunnel", "--url", "ssh://localhost:22",
            "--logfile", "cloudflared.log", "--metrics", "localhost:49589"],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    time.sleep(4)
    if cfd_proc.poll() != None:
        raise RuntimeError("Failed to run cloudflared. Return code:" +
                           str(cfd_proc.returncode) + "\nSee clouldflared.log for more info.")
    hostname = None
    # Sometimes it takes long time to display user host name in cloudflared metrices.
    for _ in range(20):
        with urllib.request.urlopen("http://127.0.0.1:49589/metrics") as response:
            text = str(response.read())
            sub = "\\ncloudflared_tunnel_user_hostnames_counts{userHostname=\"https://"
            begin = text.find(sub)
            if begin == -1:
                time.sleep(10)
                print("Retry reading cloudflared user hostname")
                continue
            end = text.index("\"", begin + len(sub))
            hostname = text[begin + len(sub): end]
            break
    if hostname == None:
        raise RuntimeError("Failed to get user hostname from cloudflared")

    ssh_common_options = "-o UserKnownHostsFile=/dev/null -o VisualHostKey=yes"
    ssh_common_options += " -oProxyCommand=\"cloudflared access ssh --hostname %h\""

    msg += "---\n"
    msg += "Command to connect to the ssh server:\n"
    msg += "✂️"*24 + "\n"
    ssh_command = f"ssh {ssh_common_options} root@{hostname}"
    msg += f"{ssh_command}\n"
    msg += "✂️"*24 + "\n"
    return msg, ssh_command
