from datetime import datetime

import pytest
from lib.archive_manager import ArchiveItem, ArchiveManager


class TestArchiveManager():

    def test_serialization(self):
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        item = ArchiveItem("global", "1", "1", "hadithText", "Content",
                           "comment", "me@email.com", "me@email.com", False, now)

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
        assert item.is_approved == False
        assert item.modified_on == now

    def test_archive_read(self, dynamodb):
        manager = ArchiveManager(dynamodb, "HadithCorrectionsArchive")
        assert len(manager.read()) == 1

    def test_write(self, dynamodb):
        manager = ArchiveManager(dynamodb, "HadithCorrectionsArchive")
        manager.write(ArchiveItem("global", "1", "1", "hadithText", "Content",
                                  "comment", "me@email.com", "me@email.com", False))

        assert len(manager.read(2)) == 2

    def test_read_n_items(self, dynamodb):
        manager = ArchiveManager(dynamodb, "HadithCorrectionsArchive")
        for i in range(5):
            manager.write(ArchiveItem("global", str(i), str(i), "hadithText", "Content",
                                      "comment", "me@email.com", "me@email.com", True))

        assert len(manager.read(4)) == 4
        assert len(manager.read(3)) == 3
