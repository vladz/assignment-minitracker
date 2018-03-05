import logging
from typing import Union

from aiohttp import web

from .routers import setup_routes

logger = logging.getLogger(__name__)

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


def main(port: Union[int, str] = 8765, debug: bool = False) -> None:
    logger.info('Tracker starting')
    tracker_app = web.Application(debug=debug)
    setup_routes(tracker_app)
    web.run_app(tracker_app, port=port)
