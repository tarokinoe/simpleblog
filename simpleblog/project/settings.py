from aiopg.sa import create_engine


DB = {
    'database': 'simpleblog',
    'user': 'simpleblog',
    'password': 'simpleblog',
    'host': 'localhost',
    'port': 5432,
}

DB_ENGINE = create_engine(**DB)

SERVER = {
    'host': 'localhost',
    'port': 8080
}