import json


def null_check(value):
    if value is None:
        return False
    if isinstance(value, dict) and len(value) >= 0:
        return True


class FieldQuery:
    """
    Field Query parameters for specific field search.
    Ex. "<field_name>": {
            "query": "field value search for",
            "fuzziness": "AUTO",
            "fuzzy_transpositions": true,
            "max_expansions": 50,
            "prefix_length": 0,
            "operator":  "or",
            "minimum_should_match": 2,
            "analyzer": "standard"
      }
    """
    query: str
    analyzer: str
    fuzziness: str
    operator: str
    fuzzy_transpositions: bool
    minimum_should_match: int
    zero_terms_query: str
    lenient: bool
    prefix_length: int
    max_expansions: int
    boost: int

    def __init__(self, query_string, analyzer="standard", fuzziness="AUTO", operator="AND", fuzzy_transpositions=True,
                 minimum_should_match=1, zero_terms_query="none", lenient=False, prefix_length=0, max_expansions=50,
                 boost=1):
        self.query = query_string
        self.analyzer = analyzer
        self.fuzziness = fuzziness
        self.operator = operator
        self.fuzzy_transpositions = fuzzy_transpositions
        self.minimum_should_match = minimum_should_match
        self.zero_terms_query = zero_terms_query
        self.lenient = lenient
        self.prefix_length = prefix_length
        self.max_expansions = max_expansions
        self.boost = boost

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class MultiMatchQuery:
    """
    Field Query parameters for specific field search.
    Ex. {
          "query": "wind",
          "fields": ["title^4", "description"],
          "type": "most_fields",
          "operator": "and",
          "minimum_should_match": 3,
          "tie_breaker": 0.0,
          "analyzer": "standard",
          "boost": 1,
          "fuzziness": "AUTO",
          "fuzzy_transpositions": true,
          "lenient": false,
          "prefix_length": 0,
          "max_expansions": 50,
          "auto_generate_synonyms_phrase_query": true,
          "zero_terms_query": "none"
        }
    """
    query: str
    fields: list[str]
    type: str
    analyzer: str
    fuzziness: str
    operator: str
    tie_breaker: float
    fuzzy_transpositions: bool
    minimum_should_match: int
    zero_terms_query: str
    lenient: bool
    prefix_length: int
    max_expansions: int
    boost: int
    auto_generate_synonyms_phrase_query: bool

    def __init__(self, query_string, fields, analyzer="standard", fuzziness="AUTO", operator="OR",
                 fuzzy_transpositions=True, tie_breaker=0.0, auto_generate_synonyms_phrase_query=True,
                 minimum_should_match=1, zero_terms_query="none", lenient=False, prefix_length=0, max_expansions=50,
                 boost=1):
        self.query = query_string
        self.fields = fields
        self.analyzer = analyzer
        self.fuzziness = fuzziness
        self.operator = operator
        self.fuzzy_transpositions = fuzzy_transpositions
        self.minimum_should_match = minimum_should_match
        self.zero_terms_query = zero_terms_query
        self.lenient = lenient
        self.prefix_length = prefix_length
        self.max_expansions = max_expansions
        self.boost = boost
        self.tie_breaker = tie_breaker
        self.auto_generate_synonyms_phrase_query = auto_generate_synonyms_phrase_query

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class Shape:
    """
    Shape dictionary object used while filtering the documents using geo_shape query.
    Ex. "geo_shape": {
            "field_name": {
              "shape": {
                "type": "envelope",
                "coordinates": [
                  [12.977406956551762,77.77235289515326],
                  [12.980947128174432,77.76651272593915]
                ]
              },
              "relation": "intersects"
            }
          }
    """
    __key__ = "shape"
    type: str
    coordinates: list[list[float]]
    relation: str

    def __init__(self, coordinates, relation, shape_type="envelope"):
        self.type = shape_type
        self.coordinates = coordinates
        self.relation = relation

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {self.__key__: {key: value for key, value in self.__dict__.items()}}


class Filter:
    """
    Builds Filter query clause, and it supports geo_distance, geo_shape geo queries.
    """
    __key__ = "filter"

    def __init__(self):
        self.geo_shape = None
        self.geo_distance = None
        self.term = None

    def add_term(self, field: str, value: str):
        self.term = {field: value}
        return self

    def add_geo_shape(self, field: str, shape: Shape):
        """
        Adds geo_shape query to filter query.
        Ex. "geo_shape": {
                "point": {
                  "shape": {
                    "type": "envelope",
                    "coordinates": [
                      [12.977406956551762,77.77235289515326],
                      [12.980947128174432,77.76651272593915]
                    ]
                  },
                  "relation": "intersects"
                }
              }
        """
        if self.geo_distance and len(self.geo_distance) > 0:
            raise TypeError("Geo Distance and Geo Shape are mutually exclusive.")
        self.geo_shape = {field: shape.to_dict()}
        return self

    def add_geo_distance(self, field: str, coordinates: list[float], distance: str, distance_type: str = "arc"):
        """
        Adds geo_distance query to filter query.
        Ex: "geo_distance": {
          "distance_type": "arc",
          "distance": "2km",
          "point": [12.978958173644923, 77.7693056800511]
        }
        """
        if self.geo_shape and len(self.geo_shape) > 0:
            raise TypeError("Geo Distance and Geo Shape are mutually exclusive.")
        self.geo_distance = {"distance_type": distance_type, "distance": distance, field: coordinates}
        return self

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class Must:
    """
    Builds must query clause to boolean query. it supports match, match_all and match_phrase clauses.
    """
    __key__ = "must"

    def __init__(self):
        self.match_all = None
        self.match = None
        self.match_phrase = None
        self.multi_match = None

    def add_match_phrase(self, field: str, value: str):
        """
        Adds Match phrase clause to boolean query.
        field: indexed document field name.
        value: filed value to be matched or unmatched.
        operator: logical operation to be applied while matching AND or OR or NOT
        Ex. "match_phrase": {
              "title": {
                "query": "wind rises the",
                "slop": 3,
                "analyzer": "standard",
                "zero_terms_query": "none"
              }
            }
        """
        if self.match_phrase is None:
            self.match_phrase = {}
        self.match_phrase[field] = {"query": value, "analyzer": "standard", "boost": 1}
        return self

    def add_match_all(self):
        """
        Adds match_all clause to boolean query.
        Ex.  "match_all": {}
        """
        if self.match_all is None:
            self.match_all = {}
        return self

    def add_match(self, field: str, value: str):
        """
        Adds match clause to boolean query.
        Ex. "match": {
              "field": "field value to search."
            }
        """
        if self.match is None:
            self.match = {}
        self.match[field] = FieldQuery(query_string=value).to_dict()
        return self

    def add_multi_match(self, fields: list[str], value: str):
        """
        Appends match query to root query.
        """
        if fields is not None and len(value) > 0:
            self.multi_match = MultiMatchQuery(query_string=value, fields=fields).to_dict()
        return self

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if null_check(value)}


class Bool:
    """
    Builds boolean query with all default values.
    Ex. "bool":{
                "must":[
                    {"match_all":{}}
                ],
                "filter":[
                    {
                        "geo_distance":
                        {
                            "distance_type":"arc",
                            "distance":"2km",
                            "point":[12.978958173644923,77.7693056800511]
                        }
                    }
                ]
            }
    """
    __key__ = "bool"

    must: list[dict]
    should: list[dict]
    must_not: list[dict]
    filter: list[dict]

    def __init__(self):
        self.must = []
        self.should = []
        self.must_not = []
        self.filter = []

    def add_must(self, must_query: Must):
        if must_query is not None:
            self.must.append(must_query.to_dict())
        return self

    def add_filter(self, filter_query: Filter):
        if filter_query is not None:
            self.filter.append(filter_query.to_dict())
        return self

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class Match:
    """
    Builds the Match query with multiple term occurrences.
    TODO: In process.
    """
    __key__ = "match"

    def __init__(self, field: str, value: str):
        """
        Adds match clause to boolean query.
        Ex. "match": {
              "field": "field value to search."
            }
        """
        self.match = {field: FieldQuery(query_string=value).to_dict()}

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class Query:
    """
    Root Query object for search query. Appends boolean & match queries to the root query.
    ex. "query": {"bool":{}} or "query": {"match":{}}
    TODO: add match_phrase, multi_match clauses to query.
    """
    __key__ = "query"

    def __init__(self):
        self.bool = {}
        self.match = {}

    def add_bool(self, bool_query: Bool):
        """
        Appends boolean query to root query.
        """
        if bool_query is not None:
            self.bool = bool_query.to_dict()
        return self

    def add_match(self, field: str, value: str):
        """
        Appends match query to root query.
        """
        if field is not None:
            self.match = {field: FieldQuery(query_string=value).to_dict()}
        return self

    def to_dict(self) -> dict:
        """
        Returns object as dictionary (key, value pairs) and ignores the keys with None.
        """
        return {key: value for key, value in self.__dict__.items() if value}


class QueryBuilder:
    """
    Query Builder Helper class, to generate OpenSearch queries dynamically.
    It also supports pagination through from and size parameters.
    """

    def __init__(self, frm=None, size=None):
        self.offset = frm
        self.limit = size
        self.query = None

    def add_query(self, query_root: Query):
        """
        Add Root Query to the search query.
        Ex. {"from": 0, "size": 20, "query": {}}
        """
        self.query = query_root.to_dict()
        return self

    def build(self) -> str:
        """
        Builds the final query and returns as string.
        """
        mapping = {'offset': 'from', 'limit': 'size'}
        return json.dumps({mapping.get(k, k): v for k, v in self.__dict__.items()})

# if __name__ == "__main__":
#     query = QueryBuilder(frm=0, size=100) \
#         .add_query(query_root=Query()
#                    .add_bool(bool_query=Bool()
#                              .add_must(must_query=Must().add_match_all())
#                              .add_filter(filter_query=Filter()
#                                          .add_geo_distance(field="point",
#                                                            coordinates=[12.978958173644923, 77.7693056800511],
#                                                            distance_type="arc",
#                                                            distance="2km")))) \
#         .build()
#
#     print(query)
