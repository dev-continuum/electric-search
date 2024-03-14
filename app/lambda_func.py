import asyncio
import json

from pydantic import ValidationError

from app import get_os_search_service
from app.dependencies import inject_logger
from app.exception.customexception import SearchException
from app.search.schema import CSSearchRequest

logger = inject_logger(name="app.lambda_func")


class LambdaError:

    def __init__(self, code, message, detail_error=None):
        self.code = code
        self.message = message
        self.detail_error = detail_error


def handler(event, context):
    """
    Lambda handler function, incoming event should compile with the schema.CSSearchRequest object.
    event: {
            "offset": 0,
            "limit": 100,
            "location": [2.3, 4.5 ],
            "proximity_in_km": 2,
            "search_by": {
                "text": "some text"
                "pincode": "560067",
                "area": null,
                "name": null,
                "charger_point_type": null,
                "power_capacity": null,
                "connector_status": null,
                "avg_rating": null
            }
        }
    """
    logger.info("Lambda Request ID: %s", context.aws_request_id)
    logger.info("Event data: %s", str(event))
    return process_request(event)


def validate_input(cs_request):
    if cs_request.location is None and cs_request.search_by is None:
        raise SearchException(code=400, message="Either Location or searchBy criteria is mandatory.")

    if cs_request.location is not None:
        if not (-90 < cs_request.location[0] < 90):
            raise SearchException(code=400, message="Invalid latitude.")
        if not (-180 < cs_request.location[0] < 180):
            raise SearchException(code=400, message="Invalid longitude.")


def process_request(event):
    try:
        cs_request = CSSearchRequest(**event)
        validate_input(cs_request)
        cs_result = asyncio.run(get_os_search_service().search(cs_request))
        logger.info("Result size: %d", cs_result.total)
        logger.info("OpenSearch took: %d", cs_result.took)
        return json.dumps(cs_result, default=lambda o: o.__dict__)
    except ValidationError as ve:
        logger.error(ve)
        return json.dumps(LambdaError(code=400, message="Invalid Input", detail_error=ve.json()).__dict__)
    except SearchException as se:
        logger.error(se)
        return json.dumps(LambdaError(code=se.code, message=se.message, detail_error=se.detail_error).__dict__)
    except Exception as e:
        logger.error(e)
        return json.dumps(LambdaError(code=500, message="Internal Server Error", detail_error=str(e)).__dict__)

# if __name__ == "__main__":
#     ctx = {"aws_request_id": "12"}
#     event = {'offset': 0, 'limit': 100, 'location': [8.561339, 76.911983], 'proximity_in_km': 2,
#              'search_by': {'text': 'Test', 'pincode': '560067', 'area': None, 'name': 'Avol',
#                            'charger_point_type': None,
#                            'power_capacity': None, 'connector_status': None, 'avg_rating': None}}
#
#     print(handler(event=event, context=ctx))
