from typing import Union, Dict, Tuple, NamedTuple
from math import hypot


class GeoPoint(NamedTuple):
    latitude: float
    longitude: float

    def distance(self, point: Union['GeoPoint', Tuple[float, float]]):
        if isinstance(point, (tuple, list)):
            point = GeoPoint(*map(float, point))
        return hypot(self.latitude - point.latitude, self.longitude - point.longitude)


class Car:
    last_car_id = 0
    car_index: Dict[int, object] = {}
    coords_index: Dict['GeoPoint', object] = {}

    def __init__(self):
        self.car_id = Car.last_car_id
        Car.last_car_id += 1
        Car.car_index[self.car_id] = self
        self._track = []

    @property
    async def coords(self) -> 'GeoPoint':
        if self._track:
            return self._track[-1]

    async def add_coords(self, point: Union['GeoPoint', Tuple[float, float]]):
        if isinstance(point, (tuple, list)):
            point = GeoPoint(*map(float, point))
        self._track.append(point)
