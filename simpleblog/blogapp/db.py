from project.utils import dictfetchall


POST_TEXT_MAX_LENGTH = 1000
POSTS_LIMIT = 12
TAG_MAX_LENGTH = 20
DESC = 'DESC'
ASC = 'ASC'


async def user_exists(conn, user_id):
    for row in await conn.execute(
        """
        select * from users where id = %s
        """,
        (user_id,)
    ):
        return True if row else False


async def create_user(conn, username):
    await conn.execute(
        "insert into users (username) values (%s)",
        (username,)
    )


async def create_post(conn, user_id, title, text, tags, date_created):
    await conn.execute(
        "insert into posts (author_id, title, text, tags, date_created) "
        "values (%s, %s, %s, %s, %s)",
        (user_id, title, text, tags, date_created)
    )


async def get_user_post(conn, user_id, order, limit=POSTS_LIMIT):
    order = ASC if order == 'asc' else DESC
    sql = ("select * from posts "
           "where author_id=%s "
           "order by date_created {order} "
           "limit %s".format(order=order))
    result = await conn.execute(sql, (user_id, limit))
    posts = await dictfetchall(result)
    return posts


async def get_posts(conn, tags=None, begin=None, end=None, order='desc',
                    title="", limit=POSTS_LIMIT):
    order = ASC if order == 'asc' else DESC
    sql = "select * from posts "
    where = []
    params = {'limit': limit}
    if tags:
        where.append("tags && %(tags)s::varchar[]")
        params['tags'] = tags
    if title:
        where.append("title ILIKE %(title)s")
        params['title'] = '%' + title + '%'
    if begin:
        where.append("date_created >= %(begin)s")
        params['begin'] = begin
    if end:
        where.append("date_created <= %(end)s")
        params['end'] = end
    if where:
        where_sql = "where " + " and ".join(where)
        sql += where_sql
    sql += (" order by date_created {order} "
            "limit %(limit)s".format(order=order))

    result = await conn.execute(sql, params)
    posts = await dictfetchall(result)
    return posts
