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
        return collection.find(query)


class PIPRankingDenunciasIntegraDAO(GenericMongoDAO):
    uri = settings.MONGO_INTEGRA_URI
    collection_name = settings.MONGO_INTEGRA_DB

    @classmethod
    def get_assuntos_orgao(cls, orgao_id):
        query = {'controleMP.movimentos.0.idOrgao': orgao_id}
        collection = cls.get(query)
        return list(collection)
