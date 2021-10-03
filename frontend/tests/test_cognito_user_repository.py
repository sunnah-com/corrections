import unittest

from lib.data.user_repository import CognitoUserRepository
from lib.mocks import CognitoMock


class TestCognitoUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock = CognitoMock()
        self.repository = CognitoUserRepository(
            "abc", "def", "ghi", "jkl"
        )
        self.repository.cognito = self.mock

    def test_list(self):
        self.mock.list_users_responses.append({
            "Users": [{
                "Username": "user1"
            }]
        })

        result = self.repository.list()

        self.assertListEqual(result, ["user1"])


if __name__ == "__main__":
    unittest.main()
