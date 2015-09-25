import json
import datetime

from peewee import *

db = SqliteDatabase(None)


class JSONField(TextField):
    db_field = "text"

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        return json.loads(value)



class Provider(Model):
    name = CharField(unique=True)
    module = CharField()
    enabled = BooleanField(default=True)
    settings = JSONField(default={})
    generate_queries = BooleanField(default=False)
    query_url = CharField()
    base_url = CharField()
    search_types = JSONField(default=[])  # todo: getters/setters for these
    search_ids = JSONField(default=[])

    class Meta:
        database = db


class ProviderSearch(Model):
    provider = ForeignKeyField(Provider)
    time = DateTimeField(default=datetime.datetime.utcnow())

    query = CharField(null=True)
    query_generated = BooleanField(default=False)
    identifier_key = CharField(null=True)
    identifier_value = CharField(null=True)
    categories = JSONField(default=[])
    season = IntegerField(null=True)
    episode = IntegerField(null=True)

    successful = BooleanField(default=False)
    results = IntegerField(null=True)  # number of results returned

    class Meta:
        database = db  # This model uses the "people.db" database.


class ProviderApiAccess(Model):
    provider = ForeignKeyField(Provider)
    time = DateTimeField(default=datetime.datetime.utcnow())
    type = CharField()  # search, download, comments, nfo?
    response_successful = BooleanField(default=False)
    response_time = IntegerField(null=True)
    error = CharField(null=True)

    class Meta:
        database = db


class ProviderSearchApiAccess(Model):
    search = ForeignKeyField(ProviderSearch)
    api_access = ForeignKeyField(ProviderApiAccess)

    class Meta:
        database = db
