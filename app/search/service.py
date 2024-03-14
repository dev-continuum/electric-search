import logging

from opensearchpy import OpenSearch

from app.exception.customexception import SearchException
from app.helper.esqueryhelper import QueryBuilder, Query, Bool, Must, Filter
from app.search.schema import CSSearchRequest, CSSearchResult, CSDocs


def add_filter_clause(field, value):
    if value:
        return Filter().add_term(field=field, value=value.lower())
    else:
        return None


def add_multi_match_clause(value):
    if value and len(value) > 0:
        return Must().add_multi_match(fields=["name",
                                              "address_line",
                                              "town",
                                              "state",
                                              "country",
                                              "total_charger_data.charger_point_type",
                                              "total_charger_data.connectors.status"], value=value)
    else:
        return None


def add_geo_clause(request):
    if request.location is not None:
        return Filter().add_geo_distance(field="geo_address",
                                         coordinates=request.location,
                                         distance_type="arc",
                                         distance="{}km".format(request.proximity_in_km))
    else:
        return None


def build_query(request: CSSearchRequest) -> str:
    """
    Method to build dynamic OS Query with the requested filters.
    Refer: helper#esqueryhelper.py and play with main method for better understanding.
    """

    qb = QueryBuilder(frm=request.offset, size=request.limit)
    qb.add_query(query_root=Query()
                 .add_bool(bool_query=Bool()
                           .add_must(must_query=add_multi_match_clause(request.search_by.text))
                           .add_filter(filter_query=add_filter_clause("name", request.search_by.name))
                           .add_filter(filter_query=add_filter_clause("address_line", request.search_by.area))
                           .add_filter(filter_query=add_filter_clause("country", request.search_by.country))
                           .add_filter(filter_query=add_filter_clause("state", request.search_by.state))
                           .add_filter(filter_query=add_filter_clause("town", request.search_by.city))
                           .add_filter(filter_query=add_filter_clause("rating.avg_rating",
                                                                      request.search_by.avg_rating))
                           .add_filter(filter_query=add_filter_clause("total_charger_data.charger_point_type",
                                                                      request.search_by.charger_point_type))
                           .add_filter(filter_query=add_filter_clause("postal_code", request.search_by.pincode))
                           .add_filter(filter_query=add_filter_clause("total_charger_data.power_capacity",
                                                                      request.search_by.power_capacity))
                           .add_filter(filter_query=add_filter_clause("total_charger_data.connectors.status",
                                                                      request.search_by.connector_status))
                           .add_filter(filter_query=add_geo_clause(request))))
    return qb.build()


class CSSearchService:
    __index_name__ = "charging_stations"

    def __init__(self, os_client: OpenSearch, logger: logging.Logger):
        self.os_client = os_client
        self.logger = logger

    """
    Search Service Implementation class.
    All Business logic goes here.
    """

    async def search(self, request: CSSearchRequest) -> CSSearchResult:
        # Use os_client to search
        if request is None:
            raise SearchException(code=400, message="Invalid request, Search Request body cannot be null.")
        query = build_query(request)
        print(query)
        try:
            response = self.os_client.search(
                body=query,
                index=CSSearchService.__index_name__
            )

            if response["hits"] is None:
                raise SearchException(code=404, message="No Records found for filter criteria.")

            docs = []
            for rec in response["hits"]["hits"]:
                doc = CSDocs(
                    id=rec["_id"],
                    score=rec["_score"],
                    charge_station=rec["_source"]
                )
                docs.append(doc)
        except Exception as e:
            raise SearchException(code=500, message="Internal server error while searching", detail_error=str(e))
        cs_result = CSSearchResult(
            took=response["took"],
            total=response["hits"]["total"]["value"],
            max_score=response["hits"]["max_score"] if response["hits"]["max_score"] else 0.0,
            records=docs
        )
        return cs_result
