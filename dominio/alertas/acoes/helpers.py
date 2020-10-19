from datetime import date


def lista_procs_ausentes(lista_procs, key_name="proc_numero_serial"):
    values = [row[key_name] for row in lista_procs]
    return [v for v in range(1, max(values)) if v not in values]


def formata_ros_ausentes(lista_numeros, num_delegacia, ano=None):
    if ano is None:
        ano = date.today().year

    return [
        f"{str(num_delegacia).zfill(3)}-{str(num).zfill(5)}/{ano}"
        for num in lista_numeros
    ]


def ros_ausentes(lista_numeros, num_delegacia, ano=None):
    return formata_ros_ausentes(
        lista_procs_ausentes(lista_numeros),
        num_delegacia=num_delegacia,
        ano=ano
    )
