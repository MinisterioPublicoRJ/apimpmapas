from django.conf import settings

from dominio.dao import GenericDAO


class MinutaPrescricaoDAO(GenericDAO):
    QUERIES_DIR = settings.BASE_DIR.child("dominio", "documentos", "queries")
    columns = [
        "num_procedimento",
        "data_fato",
        "tempo_passado",
        "assunto_docto",
        "lei_docto"
    ]
