from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from aiohttp.pytest_plugin import TestClient


async def test_add_new_car(cli: 'TestClient'):
    sended_data = json.dumps({'lat': 1, 'long': 1})
    received_data = json.dumps({'car_id': 0}, indent=4)
    resp = await cli.post('/', data=sended_data)
    assert resp.status == 201
    assert await resp.text() == received_data


async def test_get_car_list(cli: 'TestClient'):
    received_data = json.dumps({'cars': [{'id': 0}]}, indent=4)
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == received_data


async def test_change_car_coords(cli: 'TestClient'):
    sended_data = json.dumps({'lat': 2, 'long': 2})
    received_data = 'ok'
    resp = await cli.put('/0', data=sended_data)
    assert resp.status == 201
    assert await resp.text() == received_data


async def test_get_car_coords(cli: 'TestClient'):
    received_data = json.dumps({'lat': 2., 'long': 2.}, indent=4)
    resp = await cli.get('/0')
    assert resp.status == 200
    assert await resp.text() == received_data


async def test_find_nearest_car_post_m(cli: 'TestClient'):
    sended_data = json.dumps({'count': 1, 'lat': 2., 'long': 3.}, indent=4)
    received_data = json.dumps([[1., 0]], indent=4)
    resp = await cli.post('/nearest/', data=sended_data)
    assert resp.status == 200
    assert await resp.text() == received_data


async def test_find_nearest_car_get_m(cli: 'TestClient'):
    received_data = json.dumps([[1., 0]], indent=4)
    resp = await cli.get('/nearest/?count=1&lat=2&long=3')
    assert resp.status == 200
    assert await resp.text() == received_data
