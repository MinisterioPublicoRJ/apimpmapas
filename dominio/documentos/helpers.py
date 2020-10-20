from datetime import date
from io import BytesIO
from math import ceil

from openpyxl import Workbook


def formata_pena(pena):
    ano = int(pena)
    mes = ceil((pena - ano) * 12)

    pena_info = ""
    if ano > 0:
        ano_txt = "anos" if ano > 1 else "ano"
        pena_info += f"{ano} {ano_txt}"
    if mes > 0:
        mes_txt = "meses" if mes > 1 else "mês"
        if ano > 0:
            pena_info += f" e {mes} {mes_txt}"
        else:
            pena_info += f"{mes} {mes_txt}"

    return pena_info


def formata_lista(lista):
    if len(lista) > 1:
        f_lista = ", ".join(lista[:-1]) + f" e {lista[-1]}"
    else:
        f_lista = f"{lista[0]}"

    return f_lista


def traduz_mes(txt):
    meses = {
        "January": "janeiro",
        "February": "fevereiro",
        "March": "março",
        "April": "abril",
        "May": "maio",
        "June": "junho",
        "July": "julho",
        "August": "agosto",
        "September": "setembro",
        "October": "outubro",
        "November": "novembro",
        "December": "dezembro",
    }
    for mes_ingles, mes_pt in meses.items():
        txt = txt.replace(mes_ingles, mes_pt)

    return txt


def lista_procs_ausentes(lista_procs, key_name="proc_numero_serial"):
    values = [row[key_name] for row in lista_procs]
    return [v for v in range(1, max(values)) if v not in values]


def formata_ros_ausentes(lista_numeros, num_delegacia, ano=None):
    if ano is None:
        ano = date.today().year

    return [
        (id_, f"{str(num_delegacia).zfill(3)}-{str(num).zfill(5)}/{ano}")
        for id_, num in enumerate(lista_numeros, 1)
    ]


def ros_ausentes(lista_numeros, num_delegacia, ano=None):
    return formata_ros_ausentes(
        lista_procs_ausentes(lista_numeros),
        num_delegacia=num_delegacia,
        ano=ano
    )


def gera_planilha_excel(rows, header, sheet_title):
    workbook = Workbook()
    sheet = workbook[workbook.sheetnames[0]]
    sheet.title = sheet_title
    # Escreve cabeçalho
    sheet.append(header)
    for row in rows:
        sheet.append(row)

    buffer_ = BytesIO()
    workbook.save(buffer_)
    buffer_.seek(0)
    return buffer_
