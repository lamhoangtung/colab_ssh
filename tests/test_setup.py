import unittest
import os
from colab_ssh import setup_ssh


class TestSetup(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        print("Running config test")

    def test_setup(self):
        ssh_public_key = os.environ.get("TEST_SSH_PUBLIC_KEY")
        setup_ssh(ssh_public_key)
        assert 1 == 1

    def test_setup_with_notifications(self):
        webhook_address = os.environ.get("TEAMS_WEBHOOK_ADDRESS")
        ssh_public_key = os.environ.get("TEST_SSH_PUBLIC_KEY")
        setup_ssh(ssh_public_key, webhook_address)
        assert 1 == 1

if __name__ == '__main__':
    unittest.main()
