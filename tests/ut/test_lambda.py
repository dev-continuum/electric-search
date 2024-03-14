import unittest
from unittest.mock import MagicMock, Mock

from app import lambda_func
from app.search.schema import CSSearchResult


class LambdaTest(unittest.TestCase):

    @unittest.skip("Service Mocking is not happening in lambda_func. :(")
    def test_something(self):
        mock_cs = Mock()
        mock_cs.search = Mock(return_value=CSSearchResult(took=15, total=0, max_score=0))
        mock = MagicMock()
        mock.get_os_search_service().return_value = mock_cs
        cs_res = lambda_func.process_request({"from": 0, "limit": 20, "location": [12.2525, -77.5266]})
        self.assertIsNotNone(cs_res)


if __name__ == '__main__':
    unittest.main()
