import unittest
import boto3
from moto import mock_dynamodb2
from lib.data.user_repository import UserRepository

def create_mock_user_table(dynamodb):
    table = dynamodb.create_table(
    TableName='UserMock',
    KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='UserMock')
    assert table.table_status == 'ACTIVE'
    return table


@mock_dynamodb2
class TestUserRepository(unittest.TestCase):

    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table = create_mock_user_table(self.dynamodb)
        self.user_repository = UserRepository(
            None, 'us-west-2', 'UserMock'
        )

    def tearDown(self):
        self.table.delete()
        self.dynamodb=None

    def test_table_exist(self):
        self.assertTrue(self.table)
        self.assertIn('UserMock', self.table.name)

    def test_put_user(self):
        result = self.user_repository.put('test_1', True, ['testA', 'testB'], self.table)
        self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])

        get_response = self.user_repository.get('test_1', self.table)

        self.assertEqual('test_1', get_response['username'])
        self.assertTrue(get_response['permissions']['manage_users'])

    def test_get_empty(self):
        get_response = self.user_repository.get('test_empty', self.table)
        self.assertTrue(get_response is None)

    def test_list(self):
        self.user_repository.put('test_x', False, ['testA', 'testB'], self.table)
        data = self.user_repository.list(self.table)
        self.assertTrue(len(data) > 0)


if __name__ == '__main__':
    unittest.main()
