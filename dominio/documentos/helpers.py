from math import ceil


def formata_pena(pena):
    ano = int(pena)
    mes = ceil((pena - ano) * 12)

    ano_txt = "anos" if ano > 1 else "ano"
    pena_info = f"{ano} {ano_txt}"
    if mes > 0:
        mes_txt = "meses" if mes > 1 else "mês"
        pena_info += f" e {mes} {mes_txt}"

    return pena_info


def formata_lista(lista):
    if len(lista) > 1:
        f_lista = ", ".join(lista[:-1]) + f" e {lista[-1]}"
    else:
        f_lista = f"{lista[0]}"

    return f_lista
