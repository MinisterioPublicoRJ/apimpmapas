from decouple import config
from pymongo import MongoClient


class GenericMongoDAO:
    @classmethod
    def db_connect(cls):
        client = MongoClient()


class PIPRankingDenunciasIntegraDAO(GenericMongoDAO):
    pass
