from datetime import datetime
from peewee import *
from playhouse.postgres_ext import JSONField
from .database import db


class History(Model):
    created_on = DateTimeField(default=datetime.now)
    identifier = CharField(max_length=200)
    data = JSONField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.connect()
    db.create_tables([History])
    print("Tabela History criada com sucesso!")
    db.close()
