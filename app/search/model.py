# class Connector(BaseModel):
#     """
#     Charging connector model object.
#     """
#     connector_point_id: Optional[int]
#     relay_number: Optional[int]
#     status: Optional[int]
#     tariff: Optional[float]
#
#
# class Charger(BaseModel):
#     """
#     Charger type model object.
#     """
#     charger_point_type: Optional[str]
#     id: Optional[str]
#     power_capacity: Optional[str]
#     connectors: Optional[list[Connector]]
#
#
# class ChargeStation(BaseModel):
#     """
#     Charging Station Elasticsearch document model object.
#     {
#      "station_id": "115",
#      "vendor_id": "chargemod",
#      "address_line": "pixbit",
#      "available_chargers": [
#       {
#        "charger_point_type": "AC",
#        "connectors": [
#         {
#          "connector_point_id": 1,
#          "relay_number": 111,
#          "status": 1,
#          "tariff": 125
#         }
#        ],
#        "id": 1,
#        "power_capacity": "240VAC, 15A"
#       }
#      ],
#      "country": "india",
#      "distance_unit": null,
#      "is_ocpp": false,
#      "geo_address": [12.3, 12.32],
#      "latitude": 12.3,
#      "longitude": 77.45,
#      "name": "Pixbit",
#      "postal_code": "673501",
#      "qr_code": "CM-S00115-4RXJJRGTXU",
#      "rating": {
#       "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "avg_rating": 0
#      },
#      "state": "kerala",
#      "station_status": "not_connected",
#      "station_time": {
#       "end_time": "11:59 PM", "start_time": "12:00 AM"
#      },
#      "total_connectors_available": 0,
#      "town": "calicut"
#     }
#     """
#     station_id: Optional[str]
#     vendor_id: Optional[str]
#     name: Optional[str]
#     available_chargers: Optional[list[Charger]]
#     address_line: Optional[str]
#     state: Optional[str]
#     town: Optional[str]
#     country: Optional[str]
#     postal_code: Optional[str]
#     geo_address: Optional[list[float]]
#     latitude: Optional[float]
#     longitude: Optional[float]
#     distance_unit: Optional[str]
#     is_ocpp: Optional[bool]
#     qr_code: Optional[str]
#     rating: Optional[dict[str, int]]
#     station_status: Optional[str]
#     station_time: Optional[dict[str, str]]
#     total_connectors_available: Optional[int]

# cs = ChargeStation()

# import json
# cs_json = json.dumps(cs, default=lambda o: o.__dict__, indent=4)
# print(cs_json)
