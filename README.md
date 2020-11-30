# Colab SSH

Create SSH tunel to a running colab notebook

## Usage
Create a new Colab notebook with two cell with the following content:
```python
!pip3 install colab_ssh

from colab_ssh import setupSSH, loop_forever

public_key = 'https://gist.githubusercontent.com/lamhoangtung/4fca574da11ef45869bdfea8062417b5/raw/320893c60a5a150f61481899201664761136fae7/authorized_keys'
setupSSH(public_key)
loop_forever()
```

Run it, after about 2 minutes, you will see a command to SSH to the Colab notebook instance like this:

```bash

```

Then voila ;)

## Disclaimer

This repo contains many of the configuration that I use for my day to day work so your milage may vary.

If you had any problems using this, feel free to open an issue. Otherwise, I highly recommend you to fork this repo and did some necessary modification for yourself. Thanks for checking by