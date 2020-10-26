import boto3
from typing import Dict, List
from lib.data.archive_item import ArchiveItem


class ArchiveRepository:
    def __init__(self, endpoint_url, region_name, table_name):
        dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=endpoint_url,
            region_name=region_name
        )
        self.table = dynamodb.Table(table_name)

    def read(self, number_of_items: int = 1) -> List[Dict]:
        """
        This will read a number of items from the archive records from dynamodb

        number_of_items : int
            number of items to be read default is 1
        """
        return self.table.scan(Limit=number_of_items)["Items"]

    def write(self, item: ArchiveItem) -> None:
        """
        This will write an item into the archive table of dynamodb

        item: Dict
            item to be put into the archive
        """
        self.table.put_item(Item=item.serialize())
