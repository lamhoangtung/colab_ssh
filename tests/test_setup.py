import unittest
from unittest import mock
import os
from colab_ssh import setup_ssh


@mock.patch.dict(os.environ, {"IS_TESTING_CI": "TRUE"})
class TestSetup(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        print("Running setup test")

    def test_setup(self):
        # Test setup SSH with notification
        webhook_address = os.environ.get("TEAMS_WEBHOOK_ADDRESS")
        ssh_public_key = os.environ.get("TEST_SSH_PUBLIC_KEY")
        setup_ssh(ssh_public_key, webhook_address)

if __name__ == '__main__':
    unittest.main()
