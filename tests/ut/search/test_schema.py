import unittest

from app.search.schema import CSSearchRequest, SearchBy


class MyTestCase(unittest.TestCase):
    def test_cs_request(self):
        cs = CSSearchRequest(location=[12.345, -77.3445], proximity_in_km=10)
        self.cs = cs
        self.assertEqual(10, cs.proximity_in_km)
        self.assertEqual(0, cs.offset)
        self.assertEqual(100, cs.limit)

    def test_cs_request_with_text(self):
        cs = CSSearchRequest(search_by=SearchBy(text="Ather"))
        self.cs = cs
        self.assertEqual(2, cs.proximity_in_km)
        self.assertEqual(0, cs.offset)
        self.assertEqual(100, cs.limit)
        self.assertEqual("Ather", cs.search_by.text)

    def test_cs_request_with_pincode(self):
        cs = CSSearchRequest(search_by=SearchBy(text="Ather", pincode="560067"))
        self.cs = cs
        self.assertEqual(2, cs.proximity_in_km)
        self.assertEqual(0, cs.offset)
        self.assertEqual(100, cs.limit)
        self.assertEqual("Ather", cs.search_by.text)
        self.assertEqual("560067", cs.search_by.pincode)

    def test_cs_request_with_city_available_connectors(self):
        cs = CSSearchRequest(search_by=SearchBy(connector_status="Available", area="Whitefield"))
        self.cs = cs
        self.assertEqual(2, cs.proximity_in_km)
        self.assertEqual(0, cs.offset)
        self.assertEqual(100, cs.limit)
        self.assertEqual("Available", cs.search_by.connector_status)
        self.assertEqual("Whitefield", cs.search_by.area)


if __name__ == '__main__':
    unittest.main()
