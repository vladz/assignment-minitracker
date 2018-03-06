import logging
from typing import Union

from aiohttp import web

from .routers import setup_routes

logger = logging.getLogger(__name__)

DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


def init(debug: bool = False) -> 'web.Application':
    logger.info('Tracker starting')
    app = web.Application(debug=debug)
    setup_routes(app)
    return app


def main(port: Union[int, str] = 8765, debug: bool = False) -> None:
    tracker_app = init(debug)
    web.run_app(tracker_app, port=port)
