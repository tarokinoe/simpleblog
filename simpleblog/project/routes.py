from blogapp import routes as blog_routes


def setup_routes(app):
    blog_routes.setup_routes(app)