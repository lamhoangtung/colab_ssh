# Colab SSH

Create SSH tunel to a running colab notebook

![build_status](https://github.com/lamhoangtung/colab_ssh/workflows/Colab%20SSH/badge.svg)
[![codecov](https://codecov.io/gh/lamhoangtung/colab_ssh/branch/master/graph/badge.svg)](https://codecov.io/gh/Techainer/mlchain-python)
[![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/lamhoangtung/colab_ssh/blob/master/LICENSE)

## Prerequisite
- This package only allow SSH public key authentication so you will need to prepare once. You might already had one at `~/.ssh/id_rsa.pub`. Refer [this](https://www.digitalocean.com/community/tutorials/how-to-configure-ssh-key-based-authentication-on-a-linux-server) to create a new one if you don't had once already
- In order to connect to the SSH tunel from your machine, you will need to install `cloudflared` from [here](https://developers.cloudflare.com/argo-tunnel/downloads)


## Usage

Create a new Colab notebook with a single cell with the following content:
```python
!pip3 install linus_colab_ssh

from colab_ssh import setup_ssh, loop_forever

public_key = '<YOUR_PUBLIC_SSH_KEY>'
setup_ssh(public_key)
loop_forever()
```

You can use list of public key or link to a raw text file of `authorized_keys` like [this](https://gist.githubusercontent.com/lamhoangtung/4fca574da11ef45869bdfea8062417b5/raw/320893c60a5a150f61481899201664761136fae7/authorized_keys) as well

Run it, after about 2 minutes, you will see something like this:

```bash
Command to connect to the ssh server:
✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️
ssh -o UserKnownHostsFile=/dev/null -o VisualHostKey=yes -oProxyCommand="cloudflared access ssh --hostname %h" root@economic-singapore-place-obtaining.trycloudflare.com
✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️
Or you can use the following configuration in your .ssh/config file:
✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️
Host colab
	HostName economic-singapore-place-obtaining.trycloudflare.com
	User root
	UserKnownHostsFile /dev/null
	VisualHostKey yes
	StrictHostKeyChecking no
	ProxyCommand cloudflared access ssh --hostname %h
✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️✂️```
```

Then voila ;)

Please noted that you must keep the kernel webpage connected to avoid Colab disconnect your kernel early.

## Disclaimer

This repo contains many of the configuration that I use for my day to day work so it might not be the best for you.

If you had any problems using this, feel free to open an issue. Otherwise, I highly recommend you to fork this repo and did some necessary modification for yourself. Thanks for checking by
