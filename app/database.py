from playhouse.postgres_ext import PostgresqlExtDatabase
from decouple import config


db = PostgresqlExtDatabase(
    config('DATABASE_NAME', default='dtb'),
    user=config('DATABASE_USER', default='postgres'),
    password=config('DATABASE_PASSWORD', default='postgres'),
    host=config('DATABASE_HOST', default='localhost'),
    register_hstore=False
)
