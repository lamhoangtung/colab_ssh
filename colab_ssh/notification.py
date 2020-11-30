from typing import Dict

import pymsteams


def send_notification_to_microsoft_teams(webhook_address: str, spec: Dict):
    message = pymsteams.connectorcard(webhook_address)
    message.text(
        "Hi @channel, a new colab spot instance was created! Here was it configuration:")

    section = pymsteams.cardsection()
    section.addFact("CPU", spec['cpu'])
    section.addFact("RAM", spec['ram'])
    section.addFact("GPU", spec['gpu'])
    section.addFact("Connection command", spec['ssh_command'])
    message.addSection(section)
    message.send()
