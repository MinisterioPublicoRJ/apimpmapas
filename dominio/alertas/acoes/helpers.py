from datetime import date
from io import BytesIO

from openpyxl import Workbook


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
