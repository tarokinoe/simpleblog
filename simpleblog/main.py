from aiohttp import web

from project import settings
from project.settings import DB_ENGINE
from project.routes import setup_routes


async def init_pg(app):
    engine = await DB_ENGINE
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def main():
    app = web.Application()
    app['config'] = settings
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    setup_routes(app)
    web.run_app(app, host=settings.SERVER['host'], port=settings.SERVER['port'])


if __name__ == '__main__':
    main()
