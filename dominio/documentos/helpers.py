from math import ceil


def formata_pena(pena):
    mes_txt = "mês"
    ano_txt = "ano"

    ano = int(pena)
    mes = pena - ano

    mes = ceil(mes * 12)

    if ano > 1:
        ano_txt = "anos"
    if mes > 1:
        mes_txt = "meses"

    pena_info = f"{ano} {ano_txt}"
    if mes > 0:
        pena_info += f" e {mes} {mes_txt}"

    return pena_info
