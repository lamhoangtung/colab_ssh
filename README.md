# Colab SSH

Create SSH tunel to a running colab notebook

![build_status](https://github.com/lamhoangtung/colab_ssh/workflows/Colab%20SSH/badge.svg)
[![codecov](https://codecov.io/gh/lamhoangtung/colab_ssh/branch/master/graph/badge.svg)](https://codecov.io/gh/Techainer/mlchain-python)
[![license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/lamhoangtung/colab_ssh/blob/master/LICENSE)

## Usage
Create a new Colab notebook with two cell with the following content:
```python
!pip3 install linus_colab_ssh

from colab_ssh import setup_ssh, loop_forever

public_key = 'https://gist.githubusercontent.com/lamhoangtung/4fca574da11ef45869bdfea8062417b5/raw/320893c60a5a150f61481899201664761136fae7/authorized_keys'
setup_ssh(public_key)
loop_forever()
```

Run it, after about 2 minutes, you will see a command to SSH to the Colab notebook instance like this:

```bash
ssh -o UserKnownHostsFile=/dev/null -o VisualHostKey=yes -oProxyCommand="cloudflared access ssh --hostname %h" root@newspapers-tn-funky-lime.trycloudflare.com
```

In order to use this command, you will need to install `cloudflared` from [here](https://developers.cloudflare.com/argo-tunnel/getting-started/installation)


Then voila ;)

## Disclaimer

This repo contains many of the configuration that I use for my day to day work so it might not be the best for you.

If you had any problems using this, feel free to open an issue. Otherwise, I highly recommend you to fork this repo and did some necessary modification for yourself. Thanks for checking by