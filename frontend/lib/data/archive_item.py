from datetime import datetime
from typing import Dict


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
            moderator_comment: str,
            corrected_val: str,
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
        self.moderator_comment = moderator_comment
        self.corrected_val = corrected_val
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
            "moderatorComment": self.moderator_comment,
            "correctedVal": self.corrected_val,
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
            data["moderatorComment"],
            data["correctedVal"],
            data["approved"],
        )
        if "modifiedOn" in data:
            item.modified_on = data["modifiedOn"]

        return item
