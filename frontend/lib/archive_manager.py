import boto3
from datetime import datetime
from typing import Dict, List


class ArchiveItem:
    def __init__(
            self,
            queue: str,
            id: str,
            urn: int,
            attr: str,
            val: str,
            comment: str,
            submitted_by: str,
            modified_by: str,
            is_approved: bool,
            modified_on: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ) -> None:
        self.queue = queue
        self.id = id
        self.urn = urn
        self.attr = attr
        self.val = val
        self.comment = comment
        self.submitted_by = submitted_by
        self.modified_by = modified_by
        self.modified_on = modified_on
        self.is_approved = is_approved

    def serialize(self) -> Dict:
        return {
            "queue": self.queue,
            "id": self.id,
            "urn": self.urn,
            "attr": self.attr,
            "val": self.val,
            "comment": self.comment,
            "submittedBy": self.submitted_by,
            "modifiedBy": self.modified_by,
            "modifiedOn": self.modified_on,
            "approved": self.is_approved,
        }

    @classmethod
    def deserialize(cls, data: Dict):
        item = ArchiveItem(
            data["queue"],
            data["id"],
            data["urn"],
            data["attr"],
            data["val"],
            data["comment"],
            data["submittedBy"],
            data["modifiedBy"],
            data["approved"],
        )
        if "modifiedOn" in data:
            item.modified_on = data["modifiedOn"]

        return item


class ArchiveManager:

    def __init__(self, dynamodb, table_name: str) -> None:
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
