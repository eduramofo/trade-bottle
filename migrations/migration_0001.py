from peewee import *
from playhouse.migrate import *
from playhouse.postgres_ext import JSONField
from app.database import db


migrator = PostgresqlMigrator(db)

def apply_migration():
    with db.atomic():
        migrate(
            migrator.add_column('history', 'identifier', CharField(max_length=200, null=True)),
            migrator.add_column('history', 'data', JSONField(null=True))
        )

if __name__ == "__main__":
    db.connect()
    apply_migration()
    db.close()
    print("Migração aplicada com sucesso!")
