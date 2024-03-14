import asyncio
import json
import logging
import unittest
from unittest.mock import MagicMock

from app import BASE_DIR
from app.search import service
from app.search.schema import CSSearchRequest, SearchBy
from app.search.service import CSSearchService

logger = logging.getLogger("test_service")

TEST_BASE_DIR = BASE_DIR.replace('/app', '/tests') + '/datasets'


class ServiceTestSuite(unittest.TestCase):

    def test_build_query_with_location(self):
        query = service.build_query(CSSearchRequest(offset=0, limit=100, location=[12.3355, -77.4355]))
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [{"geo_distance": {"distance_type": "arc",
                                                                                            "distance": "2km",
                                                                                            "geo_address":
                                                                                                [12.3355,
                                                                                                 -77.4355]}}]}}}
        self.assertIsNotNone(query)  # add assertion here
        self.assertEqual(json.dumps(expected), query)

    def test_build_query_with_location_and_pincode(self):
        query = service.build_query(CSSearchRequest(offset=0, limit=100, location=[12.3355, -77.4355],
                                                    search_by=SearchBy(pincode="560067", area="Channasandra")))
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter":
                                                                   [{"term": {"address_line": "channasandra"}},
                                                                    {"term": {"postal_code": "560067"}},
                                                                    {"geo_distance":
                                                                         {"distance_type": "arc", "distance": "2km",
                                                                          "geo_address": [12.3355, -77.4355]}}]}}}
        self.assertIsNotNone(query)  # add assertion here
        self.assertEqual(json.dumps(expected), query)

    def test_build_query_with_location_with_pincode_area(self):
        query = service.build_query(CSSearchRequest(offset=0, limit=100, location=[12.3355, -77.4355],
                                                    search_by=SearchBy(pincode=560067, area="Channasandra")))
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [{"term": {"address_line": "channasandra"}},
                                                                          {"term": {"postal_code": "560067"}},
                                                                          {"geo_distance": {"distance_type": "arc",
                                                                                            "distance": "2km",
                                                                                            "geo_address":
                                                                                                [12.3355,
                                                                                                 -77.4355]}}]}}}

        self.assertIsNotNone(query)  # add assertion here
        self.assertEqual(json.dumps(expected), query)

    def test_search(self):
        with open(TEST_BASE_DIR + '/cs_by_location.json', 'r') as cs_json:
            data = json.load(cs_json)
        mock_os_client = MagicMock()
        mock_os_client.search.return_value = data
        cs = CSSearchService(os_client=mock_os_client, logger=logger)
        cs_res = asyncio.run(cs.search(CSSearchRequest(offset=0, limit=20, location=[12.234, -77.342])))
        self.assertIsNotNone(cs_res)
        self.assertEqual(17, cs_res.took)
        self.assertEqual(7, cs_res.total)
        self.assertEqual(1.0, cs_res.max_score)

    def test_search_with_pincode(self):
        with open(TEST_BASE_DIR + '/cs_by_location_pincode.json', 'r') as cs_json:
            data = json.load(cs_json)
        mock_os_client = MagicMock()
        mock_os_client.search.return_value = data
        cs = CSSearchService(os_client=mock_os_client, logger=logger)
        cs_res = asyncio.run(cs.search(CSSearchRequest(offset=0, limit=20, search_by=SearchBy(pincode="560066"))))
        self.assertIsNotNone(cs_res)
        self.assertEqual(15, cs_res.took)
        self.assertEqual(2, cs_res.total)
        self.assertEqual(1.0296195, cs_res.max_score)

    def test_search_with_pincode_and_area(self):
        with open(TEST_BASE_DIR + '/cs_by_location_pincode_area.json', 'r') as cs_json:
            data = json.load(cs_json)
        mock_os_client = MagicMock()
        mock_os_client.search.return_value = data
        cs = CSSearchService(os_client=mock_os_client, logger=logger)
        cs_res = asyncio.run(cs.search(CSSearchRequest(offset=0, limit=20, location=[12.234, -77.342])))
        self.assertIsNotNone(cs_res)
        self.assertEqual(8, cs_res.took)
        self.assertEqual(1, cs_res.total)
        self.assertEqual(2.828109, cs_res.max_score)


if __name__ == '__main__':
    """
    Run this with command 
    $export ACTIVE_ENVIRONMENT=test 
    $python -m unittest discover -s tests
    """
    unittest.main()
