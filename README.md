# Minitracker

```python
import requests
import json
```
Добавляем новую машину с начальными координатами (1, 1), получаем её id:
```python
print(requests.post('http://localhost:8765/', data=json.dumps({'lat': 111, 'long': 111})).text)
```
Вывод списка всех машин:
```python
print(requests.get('http://localhost:8765/').text)
```
Выводим последние координаты у машины с id = 1:
```python
print(requests.get('http://localhost:8765/1').text)
```
Меняем координаты у машины с id = 1 на (22, 22):
```python
print(requests.put('http://localhost:8765/1', data=json.dumps({'lat': 22, 'long': 22})).text)
```
Вывод ближайших 3 машин к точке (11, 11):
```python
print(requests.post('http://localhost:8765/nearest/', data=json.dumps({'count': 3, 'lat': 11, 'long': 11})).text)
print(requests.get('http://localhost:8765/nearest/?count=3,lat=11,long=11').text)
```
