"""Send push notification to Microsoft Teams using webhook. Just to manage all the instance"""

import os
from typing import Dict

import pymsteams


def send_notification_to_microsoft_teams(webhook_address: str, spec: Dict):
    """
    Send push notification to Microsoft Teams using webhook. Just to manage all the instance
    """

    message = pymsteams.connectorcard(webhook_address)
    if os.environ.get("IS_TESTING_CI") is not None:
        message.text(
            "Hi @channel, a new CI/CD test for the colab ssh pip package was initialized! Here was it configuration:")
    else:  # pragma: no cover
        message.text(
            "Hi @channel, a new colab spot instance was created! Here was it configuration:")

    section = pymsteams.cardsection()
    section.addFact("CPU", spec['cpu'])
    section.addFact("RAM", spec['ram'])
    section.addFact("GPU", spec['gpu'])
    section.addFact("Hostname", spec['hostname'])
    section.addFact("Connection command", spec['ssh_command'])
    message.addSection(section)
    try:
        message.send()
    except Exception as exception:  # pylint: disable=broad-except 
        print(f"Error sending notification to Microsoft Teams: {exception}")
