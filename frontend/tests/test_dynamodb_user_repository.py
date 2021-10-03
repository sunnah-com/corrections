import unittest

from lib.data.user_repository import DynamoDbUserRepository


class TestDynamoDbUserRepository(unittest.TestCase):
    def setUp(self):
        self.repository = DynamoDbUserRepository(
            "http://dynamodb-local:8000/", "us-west-2", "Users"
        )

    def test_put_user(self):
        actions = ["action1"]
        queues = ["testA", "testB"]
        result = self.repository.put("test_1", actions, queues)
        self.assertEqual(200, result["ResponseMetadata"]["HTTPStatusCode"])

        get_response = self.repository.get("test_1")

        self.assertEqual("test_1", get_response["username"])
        self.assertListEqual(
            get_response["permissions"]["actions"], actions)
        self.assertListEqual(
            get_response["permissions"]["queues"], queues)

    def test_get_empty(self):
        get_response = self.repository.get("test_empty")
        self.assertTrue(get_response is None)

    def test_list(self):
        self.repository.put("test_x", False, ["testA", "testB"])
        data = self.repository.list()
        self.assertTrue(len(data) > 0)


if __name__ == "__main__":
    unittest.main()
