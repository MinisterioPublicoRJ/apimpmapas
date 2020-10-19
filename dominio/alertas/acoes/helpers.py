def lista_procs_ausentes(lista_procs, key_name="proc_numero_serial"):
    values = [row[key_name] for row in lista_procs]
    return [v for v in range(max(values)) if v not in values]
