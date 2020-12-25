from datetime import datetime


class CognitoMock:
    """
    A class to mock out some functions of AWS Cognito
    """

    identitities = []

    def get_id(self, *args, **kwargs) -> dict:
        username = kwargs.get("AccountId")
        user = None
        for identity in self.identitities:
            if identity["IdentityId"] == username:
                user = identity
                break
        if not user:
            user = {
                "IdentityId": username,
                "Logins": [tuple(kwargs.get("Logins"))[0]],
                "CreationDate": datetime.today().date(),
                "LastModifiedDate": datetime.today().date(),
            }
            self.identitities.append(user)
        return {"IdentityId": username}

    def list_identities(self, *args, **kwargs) -> dict:
        return {
            "IdentityPoolId": kwargs.get("IdentityPoolId"),
            "Identities": self.identitities,
            "NextToken": kwargs.get("next", ""),
        }

    def delete(self, *args, **kwargs) -> dict:
        return {
            "UnprocessedIdentityIds": [
                {
                    "IdentityId": "string",
                },
            ]
        }
