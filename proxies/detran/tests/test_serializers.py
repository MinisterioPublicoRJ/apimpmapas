from datetime import datetime

from proxies.detran.serializers import DetranSerializer


def test_serializer_result():
    result_set = [
        (
            "ABCDE",
            "123456",
            datetime(2019, 12, 6, 0, 0),
            "Nome 1",
            "Nome 2",
            "Nome 3",
            "Cidade 1",
            datetime(1970, 1, 6, 0, 0),
            "String",
            "123456",
            "Endereço",
            "Bairro",
            "Cidade",
            "Estado",
            "123456",
        )
    ]
    ser_obj = DetranSerializer(data=result_set)
    ser_data = ser_obj.data
    expected = {
        "base": "ABCDE",
        "nu_rg": "123456",
        "dt_expedicao_carteira": datetime(2019, 12, 6, 0, 0),
        "no_cidadao": "Nome 1",
        "no_paicidadao": "Nome 2",
        "no_maecidadao": "Nome 3",
        "naturalidade": "Cidade 1",
        "dt_nascimento": datetime(1970, 1, 6, 0, 0),
        "documento_origem": "String",
        "nu_cpf": "123456",
        "endereco": "Endereço",
        "bairro": "Bairro",
        "municipio": "Cidade",
        "uf": "Estado",
        "cep": "123456",
    }
    assert ser_data == expected
