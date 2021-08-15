"""Send push notification to Mattermost Channel using webhook. Just to manage all the instance"""

import json
import os
from typing import Dict

import requests

COLAB_USER_NAME = 'colab'
COLAB_USER_ICON_LINK = 'https://colab.research.google.com/img/colab_favicon_256px.png'


def send_notification_to_mattermost(webhook_address: str, spec: Dict[str, str]):
    """
    Send push notification to Mattermost using webhook. Just to manage all the instance
    """
    text = ""
    if os.environ.get("IS_TESTING_CI") is not None:
        text += "Hi @channel, a new CI/CD test for the Colab SSH pip package was initialized! Here was it configuration:"
    else:  # pragma: no cover
        text += "Hi @channel, a new Colab spot instance was created :tada::tada::tada:! Here was it configuration:"
    text += "\n\n"
    text += f"| **CPU**      | {spec['cpu']}                                                  |\n"
    text += f"|--------------|----------------------------------------------------------------|\n"
    text += f"| **RAM**      | {spec['ram']}                                                  |\n"
    text += f"| **GPU**      | {spec['gpu']}                                                  |\n"
    text += f"| **Hostname** | `{spec['hostname']}`                                           |\n"
    text += "\n"
    text += "To **connect** to it, use the following configuration in your `~/.ssh/config` file:\n"
    text += f"```ssh-config\n{spec['ssh_config']}\n```\n"
    text += "Don't forget to **comment** to this post to **claim your colab instance** now, these thing don't really grow on tree ;). ***Happy coding!***\n"
    payload = {
        "username": COLAB_USER_NAME,
        "icon_url": COLAB_USER_ICON_LINK,
        "text": text
    }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request(
            "POST", webhook_address, headers=headers, data=payload)
        response.raise_for_status()
    except Exception as ex:
        print(f"Cannot send notification to Mattermost: {ex}")
