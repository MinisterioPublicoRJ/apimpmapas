
from time import sleep
from zeep import Client
from decouple import config


CNPJ = config('CNPJ')
CHAVE = config('CHAVE')
PERFIL = config('PERFIL')
CPF = config('CPF')


def request_connector_send_search():
    try:
        return (Client("http://10.200.96.170:8080/servico.asmx?wsdl"))
    
    except :
        raise


def request_connector_receive_results():
    try:
        return (Client("http://10.200.96.170:8181/servico.asmx?wsdl"))
    
    except :
        raise


def send_search_data_rg(rg, connector):
   
    connector.service.consultarRG(CNPJ,CHAVE,PERFIL,rg, rg.zfill(10),CPF)


def receive_results_data_rg(rg, connector):
    # 0 - initial
    # 200 - everything ok
    # 404 - photo not found

    result = connector.service.BuscarProcessados(CNPJ, CHAVE, PERFIL, rg)

    try:
        photo = result[0].fotoCivil.string[0]
        return photo
        
    except:
        print(result[0].MsgRetorno)
        return None


# THE MAIN FUNCTION #
def request_data(rg, max_attempts = 3, waiting_time = 0):

    search_connector = request_connector_send_search()
    result_connector = request_connector_receive_results()
    
    attempt = 0
    photo = None

    while attempt <= max_attempts or photo is None:

        attempt += 1

        send_search_data_rg(rg, search_connector)
        
        sleep(waiting_time)

        photo = receive_results_data_rg(rg, result_connector)

    return photo

