import unittest
from univer_db.models import TeacherChairLink

from . import Session


class TestTeacherChairLink(unittest.TestCase):
    def test_get_obj(self):
        session = Session()
        links = session.query(TeacherChairLink).filter()
        print("links: %s" % links.count())
        self.assertTrue(links.count())
