from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    message: str


class SearchBy(BaseModel):
    """
    Search parameters.
    text: accepts any string, and does the like search on specified fields.
    """
    text: Optional[str]
    pincode: Optional[str]
    name: Optional[str]
    area: Optional[str]
    state: Optional[str]
    city: Optional[str]
    country: Optional[str]
    charger_point_type: Optional[str]
    power_capacity: Optional[str]
    connector_status: Optional[str]
    avg_rating: Optional[float]


class CSSearchRequest(BaseModel):
    """
   Charge Station search request object.
   Ex. {
        "offset": 0,
        "limit": 100,
        "location": [2.3, 4.5 ],
        "proximity_in_km": 2,
        "search_by": {
            "text": "some text",
            "pincode": 560067,
            "area": null,
            "name": null,
            "charger_point_type": null,
            "power_capacity": null,
            "connector_status": null,
            "avg_rating": null
        }
    }
   """
    offset: int = 0
    limit: int = 100
    location: Optional[list[float]]
    proximity_in_km: Optional[int] = 2
    search_by: Optional[SearchBy] = SearchBy()


# cs = CSSearchRequest(location=[2.3, 4.5], search_by=SearchBy(pincode=560067))
# print(cs)
# print(json.dumps(cs, default=lambda o: o.__dict__, indent=4))
# dict = {"offset": 0, "limit": 100, "location": [2.3, 4.5], "proximity_in_km": 2,
#         "search_by": {"pincode": 560067, "area": None,
#                       "name": None, "charger_point_type": None, "power_capacity": None, "connector_status": None,
#                       "avg_rating": None}}
#
# cs = CSSearchRequest(**dict)
# print(cs)


class CSDocs(BaseModel):
    id: str
    score: float
    charge_station: dict


class CSSearchResult(BaseModel):
    """
    Documents matched to filter condition.
    Total time to filter the data, and total number of records returned by query.
    Max score assigned by Opensearch engine (this will help us to optimize our indexing.).
    """
    took: float
    total: int
    max_score: float
    records: Optional[list[CSDocs]]
