from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel


class Colors(str, Enum):
    red = 'this is red'
    blue = 'this is blue'
    yellow = 'this is yellow'


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


FAKE_DB = [{'item': 'item_1'}, {'item': 'item_2'}, {'item': 'item_3'}, {'item': 'item_4'}]

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.tax + item.price
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item, q: Optional[str] = Query(None, alias='QU')):
    result = {'item_id': item_id, **item.dict()}
    result.update({'q': q})
    return result


@app.get('/items/{item_id}')
async def get_item(item_id: int = Path(..., title='The id item', ge=0, lt=100), q: List[int] = Query([])):
    result = {'item_id': item_id}
    result.update({'q': q})
    return result


@app.get('/items/')
async def get_items(start: int = 0, end: Optional[int] = 5):
    return FAKE_DB[start:end]


@app.get('/models/{color}')
async def get_color(color: Colors):
    if color == Colors.red:
        return {'color': 'my color is red'}
    if color.value == 'this is blue':
        return {'model': color, 'color': 'my color is blue'}
    return {'model': color, 'color': 'my color is yellow'}


@app.get('/files/{file_path:path}')
async def get_file(file_path: str):
    return {'path': '/' + file_path}


@app.get('/users/me')
async def get_id_user():
    return {'message': f'User number 666'}


@app.get('/users/{user_id}')
async def get_id_user(user_id: int):
    return {'message': f'User number {user_id}'}
