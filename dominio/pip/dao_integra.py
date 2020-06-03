from django.conf import settings
from pymongo import MongoClient


class GenericMongoDAO:
    uri = None
    database_name = None
    collection_name = None

    @classmethod
    def db_connect(cls):
        client = MongoClient(cls.uri)
        database = client[cls.database_name]
        return database[cls.collection_name]

    @classmethod
    def get(cls, query, projection=None):
        collection = cls.db_connect()
        return collection.find(query, projection)

    @classmethod
    def group(cls, group, match=None, unwind=None, sort=None):
        collection = cls.db_connect()
        clauses = []
        if match:
            clauses.append({'$match': match})
        if unwind:
            clauses.append({'$unwind': unwind})
        clauses.append({'$group': group})
        if sort:
            clauses.append({'$sort': sort})
        return collection.aggregate(clauses)


class PIPRankingDenunciasIntegraDAO(GenericMongoDAO):
    uri = settings.MONGO_INTEGRA_URI
    database_name = settings.MONGO_INTEGRA_DB
    collection_name = 'ip_procedimentos_stage'

    @classmethod
    def get_assuntos_orgao(cls, orgao_id):
        match = {'controleMP.movimentos.0.idOrgao': orgao_id}
        unwind = '$ocorrencias'
        group = {
            '_id': '$ocorrencias.idTipoDelito',
            'qtd': {'$sum': 1}
        }
        sort = {'qtd': -1}
        collection = cls.group(
            match=match, unwind=unwind, group=group, sort=sort
        )
        assuntos = list(collection)

        total = 0
        for assunto in assuntos:
            total += assunto['qtd']

        mais_comuns = assuntos[:3]
        prop_comum = 0.0
        total_comum = 0
        for assunto in mais_comuns:
            proporcao = assunto['qtd']/total
            prop_comum += proporcao
            total_comum += assunto['qtd']
            assunto['proporcao'] = proporcao

        mais_comuns.append({
            'qtd': total - total_comum,
            'proporcao': 1.0 - prop_comum
        })

        return mais_comuns
