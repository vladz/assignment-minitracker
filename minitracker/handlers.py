import logging
import json
import operator

from aiohttp.web import Request, Response
from aiohttp.web_exceptions import HTTPMethodNotAllowed

from .db import Car, GeoPoint

from typing import Union, Tuple, List, Dict, Callable, Coroutine

logger = logging.getLogger(__name__)

__all__ = ['RestCarCollection', 'RestCar', 'RestFunc']


class RestBase:
    METHODS = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self):
        self.methods: Dict[str, Callable[['Request', ], Coroutine]] = {}
        for method_name in RestBase.METHODS:
            method: Callable[['Request', ], Coroutine] = getattr(self, method_name.lower(), None)
            if method:
                self.register_method(method_name, method)
        logger.debug(f'{type(self)} - registered methods: {self.methods}')

    def register_method(self, method_name: str, method: Callable[['Request', ], Coroutine]) -> None:
        logger.debug(f'{type(self)} - register method: {method_name}')
        self.methods[method_name.upper()] = method

    async def handler(self, request: 'Request') -> 'Response':
        logger.info(f'Request - path: {request.path}; method: {request.method}')
        try:
            method = self.methods[request.method]
        except KeyError:
            raise HTTPMethodNotAllowed('', RestBase.METHODS)
        status, body = await method(request)
        logger.info(f'Response - status: {status}; body: {body}')
        return Response(status=status, body=body, content_type='application/json')

    @staticmethod
    def encode(data: Union[tuple, list, dict]) -> bytes:
        return json.dumps(data, indent=4).encode('utf-8')


class RestCarCollection(RestBase):
    def __init__(self):
        super().__init__()

    async def get(self, request: 'Request') -> Tuple[int, bytes]:
        status = 200
        body = self.encode({'cars': [{'id': car} for car in Car.car_index]})
        return status, body

    async def post(self, request: Request) -> Tuple[int, bytes]:
        data = await request.json()
        status: int
        body: bytes
        try:
            car = Car()
            coords = GeoPoint(data['lat'], data['long'])
            await car.add_coords(coords)
            status = 201
            body = self.encode({'car_id': car.car_id})
        except (KeyError, TypeError):
            status = 400
            body = self.encode({'check params': 400})
        finally:
            return status, body


class RestCar(RestBase):
    def __init__(self):
        super().__init__()

    async def get(self, request: 'Request') -> Tuple[int, bytes]:
        car_id = request.match_info['id']
        status: int
        body: bytes
        try:
            car_id = int(car_id)
            car: 'Car' = Car.car_index[car_id]
            coords = await car.coords
            status = 200
            body = self.encode({'lat': coords.latitude, 'long': coords.longitude})
        except (KeyError, TypeError):
            status = 404
            body = self.encode({'not found': 404})
        finally:
            return status, body

    async def put(self, request: 'Request') -> Tuple[int, bytes]:
        car_id = request.match_info['id']
        data = await request.json()
        status: int
        body: bytes
        try:
            car_id = int(car_id)
            car: Car = Car.car_index[car_id]
            coords = GeoPoint(data['lat'], data['long'])
            await car.add_coords(coords)
            status = 201
            body = b'ok'
        except (KeyError, TypeError):
            status = 404
            body = self.encode({'not found': 404})
        finally:
            return status, body


class RestFunc(RestBase):
    def __init__(self):
        super().__init__()
        self.funcs = {'/nearest/': self.nearest_car}

    @staticmethod
    async def calculate_distance(point: Tuple[float, float], cars: Dict) -> List[Tuple[float, int]]:
        result = []
        for car_id, car in cars.items():
            car_coords = await car.coords
            distance = car_coords.distance(point)
            result.append((distance, car_id))
        result.sort(key=operator.itemgetter(0))
        return result

    async def nearest_car(self, data: Dict) -> Tuple[int, bytes]:
        try:
            count = int(data.get('count', 5))
            lat = float(data['lat'])
            long = float(data['long'])
            cars = await self.calculate_distance((lat, long), Car.car_index)
            cars = cars[:count]
            if not cars:
                status = 404
                body = self.encode({'not found': 404})
            else:
                status = 200
                body = self.encode(cars)
        except (KeyError, TypeError):
            status = 400
            body = self.encode({'check params': 400})
        return status, body

    async def post(self, request: 'Request') -> Tuple[int, bytes]:
        data = await request.json()
        status, body = await self.funcs[request.path](data)
        return status, body

    async def get(self, request: 'Request') -> Tuple[int, bytes]:
        data = request.query
        status, body = await self.funcs[request.path](data)
        return status, body
