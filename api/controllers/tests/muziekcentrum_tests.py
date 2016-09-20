from unittest import TestCase
from api.controllers.muziekcentrum import Carriers


class TestMuziekcentrum(TestCase):

    def setUp(self):
        self.carriers = Carriers()

    def test_make_payload_item(self):
        row = (0, 'b', 'c', 'd')
        pl = self.carriers._make_list_payload_item(row)
        self.assertEqual('b(c)', pl['toonnaam'])
        self.assertEqual('15', str(pl['id'])[0:2])

    def test_get_full_list_of_carriers(self):
        count, payload = self.carriers.get_full_list_of_carriers(10, 0)
        self.assertGreater(count, 50000)
        self.assertEqual(len(payload), 10)

    def test_get_release_with_id(self):
        payload = self.carriers.get_release_with_id(75286)
        payload = self.carriers.get_release_with_id(89300)
        print(payload)