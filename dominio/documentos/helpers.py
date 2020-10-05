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
