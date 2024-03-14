import json
import unittest

from app.helper.esqueryhelper import QueryBuilder, Query, Bool, Must, Filter, Shape


class QueryBuilderTestCase(unittest.TestCase):

    def test_match_query(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_match(field="title", value="Title Field value")) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"match": {
            "title": {"query": "Title Field value", "analyzer": "standard", "fuzziness": "AUTO", "operator": "AND",
                      "fuzzy_transpositions": True, "minimum_should_match": 1, "zero_terms_query": "none",
                      "max_expansions": 50, "boost": 1}}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_multi_match_query_with_filter(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_filter(filter_query=Filter().add_term(field="name", value="Avol"))
                                 .add_must(must_query=Must()
                                           .add_multi_match(fields=["name", "address_line"], value="Test")))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"must": [{"multi_match": {"query": "Test",
                                                                                         "fields": ["name",
                                                                                                    "address_line"],
                                                                                         "analyzer": "standard",
                                                                                         "fuzziness": "AUTO",
                                                                                         "operator": "OR",
                                                                                         "fuzzy_transpositions": True,
                                                                                         "minimum_should_match": 1,
                                                                                         "zero_terms_query": "none",
                                                                                         "max_expansions": 50,
                                                                                         "boost": 1,
                                                               "auto_generate_synonyms_phrase_query": True}}],
                                                               "filter": [{"term": {"name": "Avol"}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_match_all(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_must(must_query=Must()
                                           .add_match_all()))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"must": [{"match_all": {}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_match(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_must(must_query=Must()
                                           .add_match(field="title", value="fake title value")))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"must": [{"match": {
            "title": {"query": "fake title value", "analyzer": "standard", "fuzziness": "AUTO", "operator": "AND",
                      "fuzzy_transpositions": True, "minimum_should_match": 1, "zero_terms_query": "none",
                      "max_expansions": 50, "boost": 1}}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_multi_match(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_must(must_query=Must()
                                           .add_multi_match(fields=["name", "address_line"], value="Test")))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"must": [{"multi_match": {"query": "Test",
                                                                                         "fields": ["name",
                                                                                                    "address_line"],
                                                                                         "analyzer": "standard",
                                                                                         "fuzziness": "AUTO",
                                                                                         "operator": "OR",
                                                                                         "fuzzy_transpositions": True,
                                                                                         "minimum_should_match": 1,
                                                                                         "zero_terms_query": "none",
                                                                                         "max_expansions": 50,
                                                                                         "boost": 1,
                                                               "auto_generate_synonyms_phrase_query": True}}]}}}
        print(self.query)
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_filter(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_filter(filter_query=Filter()
                                             .add_term(field="title", value="fake title value")))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [{"term": {"title": "fake title value"}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_filter_geo_distance(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_filter(filter_query=Filter()
                                             .add_geo_distance(field="geo_address",
                                                               coordinates=[12.324566, -77.55454564],
                                                               distance="2km")))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [
            {"geo_distance": {"distance_type": "arc", "distance": "2km", "geo_address": [12.324566, -77.55454564]}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_filter_geo_shape(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_filter(filter_query=Filter()
                                             .add_geo_shape(field="geo_address",
                                                            shape=Shape(coordinates=[
                                                                [12.982000358725655, 77.78515215905627],
                                                                [12.994461946282915, 77.77772780479991]],
                                                                relation="intersects",
                                                                shape_type="envelope"))))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [{"geo_shape": {"geo_address": {
            "shape": {"type": "envelope",
                      "coordinates": [[12.982000358725655, 77.78515215905627], [12.994461946282915, 77.77772780479991]],
                      "relation": "intersects"}}}}]}}}
        self.assertEqual(json.dumps(expected), self.query)

    def test_bool_query_with_match_geo_filters(self):
        self.query = QueryBuilder(frm=0, size=100) \
            .add_query(query_root=Query()
                       .add_bool(bool_query=Bool()
                                 .add_filter(filter_query=Must()
                                             .add_match(field="available_chargers.charger_point_type", value="AC"))
                                 .add_filter(filter_query=Filter()
                                             .add_geo_shape(field="geo_address",
                                                            shape=Shape(coordinates=[
                                                                [12.982000358725655, 77.78515215905627],
                                                                [12.994461946282915, 77.77772780479991]],
                                                                relation="intersects",
                                                                shape_type="envelope"))))) \
            .build()
        expected = {"from": 0, "size": 100, "query": {"bool": {"filter": [{"match": {
            "available_chargers.charger_point_type": {"query": "AC", "analyzer": "standard", "fuzziness": "AUTO",
                                                      "operator": "AND", "fuzzy_transpositions": True,
                                                      "minimum_should_match": 1, "zero_terms_query": "none",
                                                      "max_expansions": 50, "boost": 1}}},
            {"geo_shape": {"geo_address": {"shape": {"type": "envelope",
                                                     "coordinates": [[12.982000358725655, 77.78515215905627],
                                                                     [12.994461946282915, 77.77772780479991]],
                                                     "relation": "intersects"}}}}]}}}
        self.assertEqual(json.dumps(expected), self.query)


if __name__ == '__main__':
    """
    Run this with command 
    $export ACTIVE_ENVIRONMENT=test 
    $python -m unittest discover -s tests
    """
    unittest.main()
