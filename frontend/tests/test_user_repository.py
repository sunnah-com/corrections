import unittest
from lib.data.user_repository import LocalUserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = LocalUserRepository(
            "http://dynamodb-local:8000/", "us-west-2", "Users"
        )

    def test_put_user(self):
        result = self.repository.put("test_1", True, ["testA", "testB"])
        self.assertEqual(200, result["ResponseMetadata"]["HTTPStatusCode"])

        get_response = self.repository.get("test_1")

        self.assertEqual("test_1", get_response["username"])
        self.assertTrue(get_response["permissions"]["manage_users"])

    def test_get_empty(self):
        get_response = self.repository.get("test_empty")
        self.assertTrue(get_response is None)

    def test_list(self):
        self.repository.put("test_x", False, ["testA", "testB"])
        data = self.repository.list()
        self.assertTrue(len(data) > 0)


if __name__ == "__main__":
    unittest.main()
