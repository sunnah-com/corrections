from typing import List
import boto3


class UserRepository:

    def __init__(self, endpoint_url, region_name, table_name):
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=endpoint_url,
            region_name=region_name
        )
        self.table = dynamodb.Table(table_name)

    def delete(self, username):
        return self.table.delete_item(Key={'username': username})

    def put(self, username, manage_users, queues):
        return self.table.put_item(Item={
            'username': username,
            'permissions': {
                'manage_users': manage_users,
                'queues': queues
            }
        })

    def get(self, username):
        result = self.table.get_item(Key={'username': username})
        return result.get('Item')

    def list(self):
        response = self.table.scan()

        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = self.table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
