from aiohttp import web
from functools import partial
import datetime
import json


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)


def json_response(*args, **kwargs):
    if 'dumps' not in kwargs:
        kwargs['dumps'] = partial(json.dumps, cls=DataEncoder)
    return web.json_response(*args, **kwargs)


def err_json_response(data, *args, **kwargs):
    response = {
        'success': False,
        'response': data
    }
    return json_response(response, *args, **kwargs)


def success_json_response(data, *args, **kwargs):
    response = {
        'success': True,
        'response': data
    }
    return json_response(response, *args, **kwargs)


async def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    return [dict(row) for row in await cursor.fetchall()]