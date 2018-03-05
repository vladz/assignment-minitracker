import logging

from .handlers import RestCarCollection, RestCar, RestFunc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiohttp.web import Application

logger = logging.getLogger(__name__)


def setup_routes(app: 'Application') -> None:
    logger.info('Init routes')
    cc = RestCarCollection()
    c = RestCar()
    f = RestFunc()
    app.router.add_route('*', '/', cc.handler)
    app.router.add_route('*', '/{id}', c.handler)
    app.router.add_get('/nearest/', f.handler)
    app.router.add_post('/nearest/', f.handler)
