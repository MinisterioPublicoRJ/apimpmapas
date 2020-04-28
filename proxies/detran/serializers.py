class DetranSerializer:
    fieldnames = [
        "base",
        "nu_rg",
        "dt_expedicao_carteira",
        "no_cidadao",
        "no_paicidadao",
        "no_maecidadao",
        "naturalidade",
        "dt_nascimento",
        "documento_origem",
        "nu_cpf",
        "endereco",
        "bairro",
        "municipio",
        "uf",
        "cep",
    ]

    def __init__(self, data, fieldnames=None):
        self._data = data
        self._fieldnames = fieldnames or self.fieldnames

    def clean_data(self, data):
        return data[0]

    @property
    def data(self):
        cleaned_data = self.clean_data(self._data)
        return dict(zip(self._fieldnames, cleaned_data))
