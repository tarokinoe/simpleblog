from datetime import datetime

from aiohttp import web

from project.utils import err_json_response, success_json_response
from . import forms, db


async def create_user_view(request):
    async with request.app['db'].acquire() as conn:
        form = forms.CreateUserForm(await request.post())
        if not form.validate():
            return err_json_response(form.errors)
        await db.create_user(conn, form.username.data)
        return success_json_response('User was created')


async def create_post_view(request):
    async with request.app['db'].acquire() as conn:
        form = forms.CreatePostForm(await request.post())
        if not form.validate():
            return err_json_response(form.errors)

        user_id = form.user_id.data
        if not await db.user_exists(conn, user_id):
            return err_json_response("User does not exists")
        await db.create_post(
            conn,
            user_id=user_id,
            title=form.title.data,
            text=form.text.data,
            tags=form.tags.data,
            date_created=datetime.utcnow())
        return success_json_response('Post was created')


async def user_posts_view(request):
    async with request.app['db'].acquire() as conn:
        form = forms.UserPostForm(request.query)
        if not form.validate():
            return err_json_response(form.errors)
        user_id = int(request.match_info.get('user_id'))
        if not await db.user_exists(conn, user_id):
            return err_json_response("User does not exists")
        result = await db.get_user_post(
            conn,
            user_id=user_id,
            order=form.order.data)
        return success_json_response(result)


async def posts_view(request):
    async with request.app['db'].acquire() as conn:
        form = forms.PostListForm(request.query)
        if not form.validate():
            return err_json_response(form.errors)
        posts = await db.get_posts(conn, **form.data)
        return success_json_response(posts)
