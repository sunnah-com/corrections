import unittest
from datetime import datetime
from lib.data.archive_item import ArchiveItem
from lib.data.archive_repository import ArchiveRepository


class TestArchiveRepository(unittest.TestCase):

    def setUp(self):
        self.repository = ArchiveRepository(
            "http://dynamodb-local:8000/", 'us-west-2', 'HadithCorrectionsArchive'
        )

    def test_serialization(self):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        item = ArchiveItem("global", "1", "1", "hadithText", "Content",
                           "comment", "me@email.com", "me@email.com", "ok", "corrected value", False, now)

        assert item.serialize()
        assert item.serialize() == {
            "queue": "global",
            "id": "1",
            "urn": "1",
            "attr": "hadithText",
            "val": "Content",
            "comment": "comment",
            "submittedBy": "me@email.com",
            "modifiedBy": "me@email.com",
            "modifiedOn": now,
            "correctedVal": "corrected value",
            "moderatorComment": "ok",
            "approved": False
        }

    def test_deserialization(self):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "queue": "global",
            "id": "1",
            "urn": "1",
            "attr": "hadithText",
            "val": "Content",
            "comment": "comment",
            "submittedBy": "me@email.com",
            "modifiedBy": "me@email.com",
            "correctedVal": "corrected value",
            "moderatorComment": "ok",
            "approved": False,
            "modifiedOn": now
        }

        item = ArchiveItem.deserialize(data)
        assert item.queue == "global"
        assert item.id == "1"
        assert item.urn == "1"
        assert item.attr == "hadithText"
        assert item.val == "Content"
        assert item.comment == "comment"
        assert item.submitted_by == "me@email.com"
        assert item.modified_by == "me@email.com"
        assert item.corrected_val == "corrected value"
        assert item.moderator_comment == "ok"
        assert item.is_approved == False
        assert item.modified_on == now

    def test_read(self):
        assert len(self.repository.read()) == 1

    def test_write(self):
        self.repository.write(ArchiveItem("queue",
                                          "id",
                                          "urn",
                                          "attr",
                                          "val",
                                          "comment",
                                          "me@email.com",
                                          "guest",
                                          "ok",
                                          "corrected_val",
                                          False))

        assert len(self.repository.read(2)) == 2


if __name__ == '__main__':
    unittest.main()
