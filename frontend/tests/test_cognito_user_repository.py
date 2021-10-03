import unittest
from unittest.mock import Mock

from lib.data.user_repository import CognitoUserRepository


class TestCognitoUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = CognitoUserRepository(
            "abc", "def", "ghi", "jkl"
        )
        self.repository.cognito = Mock()

    def test_list(self):
        self.repository.cognito.list_users.return_value = {
            "Users": [{
                "Username": "user1"
            }]
        }

        result = self.repository.list()

        self.assertListEqual(result, ["user1"])


if __name__ == "__main__":
    unittest.main()
