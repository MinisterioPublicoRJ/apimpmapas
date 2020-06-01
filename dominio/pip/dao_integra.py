from pymongo import MongoClient

from mprj_api import settings


class GenericMongoDAO:
    uri = None
    database_name = None
    collection_name = None

    @classmethod
    def db_connect(cls):
        client = MongoClient(cls.uri)
        return client[cls.database_name]


    @classmethod
    def get(cls, query, projection=None):
        db = cls.db_connect()
        collection = db[cls.collection_name]
        return collection.find(query, projection)


class PIPRankingDenunciasIntegraDAO(GenericMongoDAO):
    uri = settings.MONGO_INTEGRA_URI
    database_name = settings.MONGO_INTEGRA_DB
    collection_name = 'ip_procedimentos_stage'

    @classmethod
    def get_assuntos_orgao(cls, orgao_id):
        query = {'controleMP.movimentos.0.idOrgao': orgao_id}
        projection = {'ocorrencias.idTipoDelito': 1}
        collection = cls.get(query, projection)
        return list(collection)
