import unittest
from unittest.mock import MagicMock

from lib.data.user_repository import (CognitoUserRepository,
                                      DynamoDbUserRepository, UserRepository)


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.mock_dynamodb_repository = DynamoDbUserRepository(
            "http://dynamodb-local:8000/", "us-west-2", "Users")
        self.mock_cognito_repository = CognitoUserRepository(
            "us-west-2", "access_key", "secret", "pool_id")
        self.repository = UserRepository(
            self.mock_dynamodb_repository, self.mock_cognito_repository)

    def test_list(self):
        user1 = {"username": "abc"}
        user2 = {"username": "def"}
        self.mock_dynamodb_repository.list = MagicMock(return_value=[
            user1,
            user2
        ])
        self.mock_cognito_repository.list = MagicMock(return_value=["abc"])

        result = self.repository.list()

        self.assertListEqual(result, [user1])

    def test_get(self):
        self.mock_dynamodb_repository.get = MagicMock(return_value="def")

        result = self.repository.get("abc")

        self.mock_dynamodb_repository.get.assert_called_with("abc")
        self.assertEqual("def", result)

    def test_put(self):
        self.mock_dynamodb_repository.put = MagicMock()

        self.repository.put("abc", True, ["global"])

        self.mock_dynamodb_repository.put.assert_called_with("abc",
                                                             True,
                                                             ["global"])


if __name__ == "__main__":
    unittest.main()
