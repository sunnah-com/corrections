from datetime import datetime
from typing import Deque


class CognitoMock:
    """
    A class to mock out some functions of AWS Cognito
    """

    list_users_responses = Deque()

    def list_users(self, *args, **kwargs) -> dict:
        return self.list_users_responses.popleft()
