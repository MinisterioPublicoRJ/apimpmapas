def lista_procs_ausentes(lista_procs, key_name="proc_numero_serial"):
    values = [row[key_name] for row in lista_procs]
    return [v for v in range(max(values)) if v not in values]


def formata_ros_ausentes(lista_numeros, num_delegacia, ano=None):
    return [
        f"{str(num_delegacia).zfill(3)}-{str(num).zfill(5)}/{ano}"
        for num in lista_numeros
    ]
