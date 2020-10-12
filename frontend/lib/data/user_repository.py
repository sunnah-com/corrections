from typing import List
import boto3


class UserRepository:

    def __init__(self, endpoint_url, region_name, table_name):
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        self.table_name = table_name

    def _get_table(self):
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=self.endpoint_url,
            region_name=self.region_name
        )
        table = dynamodb.Table(self.table_name)
        return table

    def delete(self, username, table=None):
        if table is None:
            table = self._get_table()

        return table.delete_item(Key={'username': username})

    def put(self, username, manage_users, queues, table=None):
        if table is None:
            table = self._get_table()

        return table.put_item(Item={
            'username': username,
            'permissions': {
                'manage_users': manage_users,
                'queues': queues
            }
        })

    def get(self, username, table=None):
        if table is None:
            table = self._get_table()
        result = table.get_item(Key={'username': username})
        return result.get('Item')

    def list(self, table):
        if table is None:
            table = self._get_table()
        response = table.scan()

        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
