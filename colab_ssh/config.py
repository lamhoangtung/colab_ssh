import subprocess
import secrets
from colab_ssh.utils import AptManager, download_file

def config_root_password(msg):
    root_password = secrets.token_urlsafe()
    subprocess.run(
        ["chpasswd"], input=f"root:{root_password}", universal_newlines=True)
    msg += "✂️"*24 + "\n"
    msg += f"Root password: {root_password}\n"
    msg += "✂️"*24 + "\n"
    return msg


def install_common_tool(msg):
    apt_manager = AptManager()
    apt_manager.commit()
    all_pkg = ['nano', 'htop', 'tmux', 'vim', 'cmake',
               'libncurses5-dev', 'libncursesw5-dev', 'git',
               'tree', 'zip', 'expect', 'pigz', 'pv']
    apt_manager.installPkg(**all_pkg)
    apt_manager.commit()

    # nvtop

    # pip3 install imgaug trains ipdb

    # Bashrc

    # gdrive

    # iterm

    # rclone

    # vim

    # tmux
