def format_text(text):
    """Formata o texto relativo ao nome das promotorias.

    Arguments:
        text {string} -- Texto a ser formatado.

    Returns:
        string -- Texto formatado.
    """
    return ' '.join(
        [
            t.capitalize() if len(t) > 3 or t == "rio"
            else t for t in text.lower().split()
        ]
    )


def get_top_n_orderby_value_as_dict(
        l, name_position=1, value_position=2, name_fieldname='nm_promotoria',
        value_fieldname='valor', n=3, cast_f=float):
    """Ordena uma lista de tuplas utilizando uma posição escolhida,
    e retorna os top N maiores em um formato de lista de dicionários
    com um campo de nome e um campo de valor.

    Arguments:
        l {list} -- Lista de dados.
        name_position {int} --Posição da tupla onde está o nome da promotoria.
        value_position {int} -- Posição da tupla onde está o valor usado
            para ordenação.
        name_fieldname {string} -- Nome do campo de nome presente nos
            dicionários finais.
        value_fieldname {string} -- Nome do campo de valor presente nos
            dicionários finais.

    Keyword Arguments:
        n {int} -- Quantidade de dados a retornar no Top N.
        cast_f {function} -- Função para castear o valor a ser utilizado.
          Usado para evitar idiossincrasias ao ordenar números representados
          como string, em especial números negativos. Default: float.

    Returns:
        List[dict] -- Lista de dicionários contendo os Top N em ordem.
    """
    sorted_list = sorted(
        l,
        key=lambda el: cast_f(el[value_position]),
        reverse=True)
    result_list = [
        {
            name_fieldname: format_text(el[name_position]),
            value_fieldname: el[value_position]
        }
        for el in sorted_list
    ]
    return result_list[:n]


def get_value_given_key(l, key_value, key_position, value_position):
    """Busca o valor associada a uma chave, em uma lista de tuplas.

    Arguments:
        l {list} -- Lista de tuplas.
        key_value -- Valor da chave a procurar.
        key_position -- Posição da chave nas tuplas.
        value_position -- Posição do valor a ser buscado nas tuplas.

    Returns:
        value -- Valor presente na lista, referente à chave dada.
    """
    for element in l:
        if element[key_position] == key_value:
            return element[value_position]
    return None
