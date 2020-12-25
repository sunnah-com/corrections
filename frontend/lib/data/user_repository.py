from typing import List
import boto3


class LocalUserRepository:
    def __init__(self, endpoint_url, region_name, table_name):
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url=endpoint_url, region_name=region_name
        )
        self.table = dynamodb.Table(table_name)

    def delete(self, username):
        return self.table.delete_item(Key={"username": username})

    def put(self, username, manage_users, queues):
        return self.table.put_item(
            Item={
                "username": username,
                "permissions": {"manage_users": manage_users, "queues": queues},
            }
        )

    def get(self, username):
        result = self.table.get_item(Key={"username": username})
        return result.get("Item")

    def list(self):
        response = self.table.scan()

        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self.table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return data


class RemoteUserRepository:
    """
    This will handle all the CRUD actions for users
    in the AWS cognito user pool
    """

    def __init__(self, endpoint_url: str, region_name: str, identity_pool_id: str):
        self.identity_pool_id = identity_pool_id
        self.provider_name = (
            f"cognito-idp.{region_name}.amazonaws.com/{identity_pool_id}"
        )
        self.cognito = boto3.client(
            "cognito-identity", endpoint_url=endpoint_url, region_name=region_name
        )

    def get_or_create(self, username: str, password: str) -> dict:
        return self.cognito.get_id(
            AccountId=username,
            IdentityPoolId=self.identity_pool_id,
            Logins={self.provider_name: password},
        )

    def list(self, limit: int = 10, next: str = "") -> dict:
        response = self.cognito.list_identities(
            IdentityPoolId=self.identity_pool_id,
            MaxResults=limit,
            NextToken=next,
            HideDisabled=True,
        )
        return response

    def delete(self, usernames: List[str]) -> dict:
        response = self.cognito.delete_identities(IdentityIdsToDelete=usernames)

        return response
