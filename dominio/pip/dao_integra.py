from pymongo import MongoClient

from mprj_api import settings


class GenericMongoDAO:
    uri = None
    collection_name = None

    @classmethod
    def db_connect(cls):
        client = MongoClient(cls.uri)
        return client[cls.collection_name]

    @classmethod
    def get(cls, query):
        collection = cls.db_connect()
        return collection.aggregate(query)


class PIPRankingDenunciasIntegraDAO(GenericMongoDAO):
    uri = settings.MONGO_INTEGRA_URI
    collection_name = settings.MONGO_INTEGRA_DB

    pass
