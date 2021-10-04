import boto3
from flask import current_app


class DynamoDbUserRepository:
    def __init__(self, endpoint_url, region_name, table_name):
        dynamodb = boto3.resource(
            "dynamodb", endpoint_url=endpoint_url, region_name=region_name
        )
        self.table = dynamodb.Table(table_name)

    def put(self, username, actions, queues):
        return self.table.put_item(
            Item={
                "username": username,
                "permissions": {
                    "actions": actions,
                    "queues": queues
                },
            }
        )

    def get(self, username):
        result = self.table.get_item(Key={"username": username})
        return result.get("Item")

    def list(self):
        response = self.table.scan()

        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self.table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return data


class CognitoUserRepository:
    """
    This will handle all the CRUD actions for users
    in the AWS cognito user pool
    """

    def __init__(self,
                 region_name: str,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 user_pool_id: str):
        self.user_pool_id = user_pool_id
        self.cognito = boto3.client(
            "cognito-idp",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    def list(self) -> dict:
        users = []
        response = self.cognito.list_users(
            UserPoolId=self.user_pool_id,
            Limit=60
        )
        pagination_token = "none"
        while pagination_token:
            users.extend(response["Users"])
            pagination_token = response.get("PaginationToken")
            if pagination_token:
                response = self.cognito.list_users(
                    UserPoolId=self.user_pool_id,
                    PaginationToken=pagination_token,
                    Limit=60
                )
        usernames = [user["Username"] for user in users]
        return usernames


class UserRepository:
    def __init__(self,
                 dynamodb_repository: DynamoDbUserRepository,
                 cognito_repository: CognitoUserRepository):
        self.dynamodb_repository = dynamodb_repository
        self.cognito_repository = cognito_repository

    def put(self, username, actions, queues):
        return self.dynamodb_repository.put(username, actions, queues)

    def get(self, username):
        return self.dynamodb_repository.get(username)

    def check_permission(self, username, action):
        user = self.dynamodb_repository.get(username)
        if not user:
            return False
        permissions = user.get("permissions", {})
        return action in permissions.get("actions", [])

    def list(self):
        cognito_usernames = self.cognito_repository.list()
        dynamodb_users = self.dynamodb_repository.list()
        users = [user for user in dynamodb_users
                 if user.get("username") in cognito_usernames]
        return users


def get_cognito_repository():
    region_name = current_app.config["REGION"]
    user_pool_id = current_app.config["AWS_COGNITO_USER_POOL_ID"]
    aws_access_key_id = current_app.config["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = current_app.config["AWS_SECRET_ACCESS_KEY"]
    repository = CognitoUserRepository(
        region_name, aws_access_key_id, aws_secret_access_key, user_pool_id)
    return repository


def get_dynamodb_repository():
    region_name = current_app.config["REGION"]
    endpoint_url = current_app.config["DYNAMODB_ENDPOINT_URL"]
    table_name = current_app.config["DYNAMODB_TABLE_USERS"]
    repository = DynamoDbUserRepository(endpoint_url, region_name, table_name)
    return repository


def get_user_repository():
    dynamodb_repository = get_dynamodb_repository()
    cognito_repository = get_cognito_repository()
    return UserRepository(dynamodb_repository, cognito_repository)
