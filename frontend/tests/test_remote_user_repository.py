import unittest
from datetime import datetime

from lib.data.user_repository import RemoteUserRepository
from lib.mocks import CognitoMock


class TestRemoteUserRepository(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.repository = RemoteUserRepository(
            "http://dynamodb-local:8000/", "us-west-2", "id"
        )
        self.repository.cognito = CognitoMock()

    def test_create_user(self):
        result = self.repository.get_or_create("user1", "password")
        self.assertDictEqual(result, {"IdentityId": "user1"})

    def test_list(self):
        self.repository.get_or_create("user2", "password")
        self.repository.get_or_create("user3", "password")
        result = self.repository.list()
        self.assertDictEqual(
            result,
            {
                "IdentityPoolId": "id",
                "Identities": [
                    {
                        "IdentityId": "user1",
                        "Logins": [
                            f"cognito-idp.us-west-2.amazonaws.com/id",
                        ],
                        "CreationDate": datetime.today().date(),
                        "LastModifiedDate": datetime.today().date(),
                    },
                    {
                        "IdentityId": "user2",
                        "Logins": [
                            "cognito-idp.us-west-2.amazonaws.com/id",
                        ],
                        "CreationDate": datetime.today().date(),
                        "LastModifiedDate": datetime.today().date(),
                    },
                    {
                        "IdentityId": "user3",
                        "Logins": [
                            "cognito-idp.us-west-2.amazonaws.com/id",
                        ],
                        "CreationDate": datetime.today().date(),
                        "LastModifiedDate": datetime.today().date(),
                    },
                ],
                "NextToken": "",
            },
        )


if __name__ == "__main__":
    unittest.main()
