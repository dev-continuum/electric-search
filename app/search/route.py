import logging

from fastapi import APIRouter, Depends

from app import get_os_search_service
from app.dependencies import inject_logger
from app.search.schema import CSSearchResult, CSSearchRequest, Message
from app.search.service import CSSearchService


def on_startup():
    print("Search Router started")


def pre_shutdown():
    print("Search Router started")


router = APIRouter(
    prefix="/search",
    on_startup=on_startup(),
    on_shutdown=pre_shutdown()
)


class RouteLogger:

    def __call__(self, name: str = "app.search.route"):
        return inject_logger(name)


route_logger = RouteLogger()


@router.get("/", response_model=CSSearchResult, responses={404: {"model": Message}})
async def get_stations(lat: float, long: float,
                       cs_service: CSSearchService = Depends(get_os_search_service),
                       logger: logging.Logger = Depends(route_logger)) \
        -> CSSearchResult:
    es_results = await cs_service.search(CSSearchRequest(location=[lat, long]))
    logger.info("Search took %d", es_results.took)
    return es_results


@router.post("/", response_model=CSSearchResult,
             responses={404: {"model": Message}})
async def search_stations(cs_search: CSSearchRequest,
                          cs_service: CSSearchService = Depends(get_os_search_service),
                          logger: logging.Logger = Depends(inject_logger)) \
        -> CSSearchResult:
    logger.info("Request for location %s", cs_search.location)
    return await cs_service.search(cs_search)
