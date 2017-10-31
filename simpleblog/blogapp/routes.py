from .views import (create_user_view, create_post_view, user_posts_view,
                    posts_view)


def setup_routes(app):
    app.router.add_get(r'/user/{user_id:\d+}/posts', user_posts_view)
    app.router.add_get(r'/posts', posts_view)
    app.router.add_post('/users/new', create_user_view)
    app.router.add_post('/posts/new', create_post_view)
