import unittest
from unittest import mock
import os

from psutil import test
from colab_ssh import setup_ssh
from colab_ssh.notification import send_notification_to_microsoft_teams
from colab_ssh.ssh import parse_public_key

@mock.patch.dict(os.environ, {"IS_TESTING_CI": "TRUE"})
class TestSetup(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        print("Running setup test")

    def test_setup(self):
        # Test setup SSH with notification
        webhook_address = os.environ.get("TEAMS_WEBHOOK_ADDRESS")
        ssh_public_key = os.environ.get("TEST_SSH_PUBLIC_KEY")
        if webhook_address is None:
            print("Lol this shit is none")
        setup_ssh(ssh_public_key, webhook_address)

    def test_fail_push_notification(self):
        webhook_address = 'lol'
        spec = {
            'cpu': 'hihi',
            'gpu': 'haha',
            'ram': 'hoho',
            'ssh_command': 'lul',
            'hostname': 'lol'
        }
        send_notification_to_microsoft_teams(webhook_address, spec)

    def test_parse_public_key(self):
        test_key = ['ssh-a', 'ssh-b', 'ssh-c']
        parsed_key = parse_public_key(test_key[0])
        assert parsed_key == test_key[:1]
        parsed_key = parse_public_key(test_key)
        assert parsed_key == test_key
        assert [] == parse_public_key(None)
        try:
            _ = parse_public_key('lol')
        except ValueError as ex:
            pass

if __name__ == '__main__':
    unittest.main()
