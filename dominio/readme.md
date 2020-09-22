# API Promotron

Documentação de acesso à API do robô das promotorias.

## Acervo

#### Volume do Acervo por órgão

```
GET dominio/acervo/<id_orgao>/<yyyy-MM-dd>
 ```

 ```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "acervo_qtd": 157
}
 ```

#### Variação do Acervo de um órgão


```
GET dominio/acervo_variation/<id_orgao>/<yyyy-MM-dd>/<yyyy-MM-dd>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "acervo_fim": 157,
    "acervo_inicio": 157,
    "variacao": 0.0
}
```

#### Maiores variações do Acervo

```
GET dominio/acervo_variation_topn/<id_orgao>/<yyyy-MM-dd>/<yyyy-MM-dd>/<n>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "cod_orgao": <int:cod_orgao>,
        "nm_orgao": <str:nm_orgao>,
        "acervo_fim": 172,
        "acervo_inicio": 172,
        "variacao": 0.0
    },
    {
        "cod_orgao": <int:cod_orgao>,
        "nm_orgao": <str:nm_orgao>,
        "acervo_fim": 186,
        "acervo_inicio": 186,
        "variacao": 0.0
    },
    {
        "cod_orgao": <int:cod_orgao>,
        "nm_orgao": <str:nm_orgao>,
        "acervo_fim": 131,
        "acervo_inicio": 131,
        "variacao": 0.0
    }
]
```

## Outliers

```
GET dominio/outliers/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "cod_orgao": <int:id_orgao>,
    "acervo_qtd": 10,
    "cod_atribuicao": <int:cod_atribuicao>,
    "minimo": 112,
    "maximo": 290,
    "media": 171.4,
    "primeiro_quartil": 140.25,
    "mediana": 153.5,
    "terceiro_quartil": 182.5,
    "iqr": 42.25,
    "lout": 76.875,
    "hout": 245.875,
    "dt_inclusao": "2020-03-20 14:28:35"
}
```


## Saídas
```
GET /dominio/saidas/<id_orgao>
```


```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "saidas": 2,
    "id_orgao": <int:id_ordao>,
    "cod_pct": 26,
    "percent_rank": 0.8888888888888888,
    "dt_calculo": "2020-02-11T16:27:09.273000Z"
}
 ```

## Sua Mesa

### Sua Mesa Integrado
```
GET /dominio/suamesa/documentos/<str:orgao_id>?tipo=tipo_de_dado&cpf=1234

CPF é opcional, dependendo do tipo de dado requisitado (ver lista abaixo).

Tipos aceitos:
- vistas: Vistas abertas para um órgão e CPF. (cpf obrigatório)
- tutela_investigacoes: Número de investigações em curso de uma tutela.
- tutela_processos: Número de processos em juízo de uma tutela.
- tutela_finalizados: Número de documentos finalizados nos últimos 30 dias em uma tutela.
- pip_inqueritos: Número de inquéritos ativos em uma PIP.
- pip_pics: Número de PICs ativas em uma PIP.
- pip_aisp: Número de inquéritos e PICs ativos na AISP de uma PIP.
- pip_finalizados: Número de documentos finalizados nos últimos 30 dias para PIPs.

Obs.: Finalizados não consideram desarquivamentos!
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "nr_documentos": 1
}
```

### Sua Mesa Detalhes Integrado
```
GET /dominio/suamesa/documentos-detalhe/<str:orgao_id>?tipo=tipo_de_dado&cpf=1234&n=3&intervalo=30

CPF (opcional) - depende do tipo de dado requisitado (ver lista abaixo).
n (opcional) - Número de promotorias para retornar no Top N. Default: 3.
intervalo (opcional) - Intervalo de tempo para olhar, caso disponível. Default: 30.

Tipos aceitos:
- tutela_investigacoes: Detalhe de investigações em curso de uma tutela.
- tutela_processos: Detalhe de processos em juízo de uma tutela.
- pip_inqueritos: Detalhe de inquéritos da PIP. (Requer CPF)
- pip_pics: Detalhe de PICs da PIP. (Requer CPF)
- pip_aisp: Detalhe de inquéritos e PICs da AISP de uma PIP.
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "metrics": {
        'dado1': 1234,
        'dado2': 1234,
    },
    "rankings": [
        {
            'ranking_fieldname': 'nome',
            'data': [{'nm_orgao': 'Orgao1', 'valor': 10}, {'nm_orgao': 'Orgao2', 'valor': 5}, ...]
        }
    ],
    "mapData: {}
}

O atributo 'valor' dos rankings pode vir como 'valor_percentual', caso seja relativo a uma porcentagem.
```

### Vistas Abertas
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/suamesa/vistas/<id_orgao>/<cpf>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "suamesa_vistas": 1
}
```

### Investigações em curso
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/suamesa/investigacoes/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "suamesa_investigacoes": 0
}
```

### Processos em juízo
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/suamesa/processos/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "suamesa_processos": 0
}
```

### Finalizados nos últimos 30 dias
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/suamesa/finalizados/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "suamesa_finalizados": 0
}
```


## Detalhe Vistas Abertas Sua Mesa

```
GET /dominio/suamesa/detalhe/vistas/<id_orgao>/<cpf>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "soma_ate_vinte": 0,
    "soma_vinte_trinta": 0,
    "soma_trinta_mais": 1
}
```

## Listas Vistas Abertas Sua Mesa

```
GET /dominio/suamesa/lista/vistas/<id_orgao>/<cpf>/<abertura>?page=<int>

valores possíveis para abertura: ate_vinte, vinte_trinta, trinta_mais

page: default=1
page_size (elementos por página): 20
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept


[
    {
        "numero_mprj": "1234567890",
        "numero_externo": "0987654321",
        "dt_abertura": "2020-01-01",
        "classe": "CLASSE 1"
    },
    {
        "numero_mprj": "0987654321",
        "numero_externo": "1234567890",
        "dt_abertura": "2020-01-01",
        "classe": "CLASSE 2"
    }
]
```

## Radar Performance

```
GET /dominio/radar/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
     "cod_pct": 123,
     "pacote_atribuicao": "Tutela Coletiva",
     "orgao_id": 12345.0,
     "nr_arquivamentos": 45,
     "nr_indeferimentos": 29,
     "nr_instauracoes": 5,
     "nr_tac": 0,
     "nr_acoes": 0,
     "max_pacote_arquivamentos": 156,
     "max_pacote_indeferimentos": 99,
     "max_pacote_instauracoes": 38,
     "max_pacote_tac": 1,
     "max_pacote_acoes": 12,
     "perc_arquivamentos": 0.28846153846153844,
     "perc_indeferimentos": 0.29292929292929293,
     "perc_instauracoes": 0.13157894736842105,
     "perc_acoes": 0.0,
     "perc_tac": 0.0,
     "med_pacote_aquivamentos": 53.5,
     "med_pacote_tac": 47.0,
     "med_pacote_indeferimentos": 20.0,
     "med_pacote_instauracoes": 0.0,
     "med_pacote_acoes": 1.5,
     "var_med_arquivamentos": -0.1588785046728972,
     "var_med_tac": -0.3829787234042553,
     "var_med_indeferimentos": -0.75,
     "var_med_instauracoes": null,
     "var_med_acoes": -1.0,
     "dt_calculo": "2020-03-30T10:46:14.837000",
     "nm_max_arquivamentos": "Promotoria de Justiça 1",
     "nm_max_indeferimentos": "Promotoria de Justiça 2, Promotoria de Justiça 3",
     "nm_max_instauracoes": "Promotoria de Justiça 4",
     "nm_max_tac": "1ª Promotoria de Justiça",
     "nm_max_acoes": "4ª Promtoria de Justiça"
}
```

## Comparação de Radares de Performance Tutela

```
GET /dominio/comparador-radares/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
  {
      "orgao_id": "3456",
      "orgao_codamp": "2ª PJ",
      "orgi_nm_orgao": "2ª PROMOTORIA",
      "perc_arquivamentos": 1.0,
      "perc_indeferimentos": 0.0,
      "perc_instauracoes": None,
      "perc_tac": 0.7,
      "perc_acoes": None
  },
  {
      "orgao_id": "6789",
      "orgao_codamp": "1ª PJ",
      "orgi_nm_orgao": "1ª PROMOTORIA",
      "perc_arquivamentos": 1.0,
      "perc_indeferimentos": 1.0,
      "perc_instauracoes": None,
      "perc_tac": 1.0,
      "perc_acoes": None
  }
]
```

## Comparação de Radares de Performance PIP

```
GET /dominio/pip/comparador-radares/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
  {
      "orgao_id": "3456",
      "orgao_codamp": "2ª PJ",
      "orgi_nm_orgao": "2ª PROMOTORIA",
      "perc_arquivamentos": 1.0,
      "perc_indeferimentos": 0.0,
      "perc_instauracoes": None,
      "perc_tac": 0.7,
      "perc_acoes": None
  },
  {
      "orgao_id": "6789",
      "orgao_codamp": "1ª PJ",
      "orgi_nm_orgao": "1ª PROMOTORIA",
      "perc_arquivamentos": 1.0,
      "perc_indeferimentos": 1.0,
      "perc_instauracoes": None,
      "perc_tac": 1.0,
      "perc_acoes": None
  }
]
```

## Tempo Tramitação

```
GET /dominio/tempo-tramitacao/<id_orgao>?version=<str>

'version' é um parâmetro opcional.
Para usar a nova versão do tempo de tramitação, usar 'version=1.1'.
Qualquer outro valor de version (ou sem version) irá usar a versão antiga.
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id_orgao": 12345,
    "media_orgao": 10.1243,
    "minimo_orgao": 0,
    "maximo_orgao": 100,
    "mediana_orgao": 10.2312,
    "media_pacote": 11.4352,
    "minimo_pacote": 0,
    "maximo_pacote": 200,
    "mediana_pacote": 56.3124,
    "media_pacote_t1": 45.343,
    "minimo_pacote_t1": 12,
    "maximo_pacote_t1": 533,
    "mediana_pacote_t1": 343.324,
    "media_orgao_t1": 344.12,
    "minimo_orgao_t1": 12,
    "maximo_orgao_t1": 5023,
    "mediana_orgao_t1": 2421.1223,
    "media_pacote_t2": 343.1254,
    "minimo_pacote_t2": 48,
    "maximo_pacote_t2": 2335,
    "mediana_pacote_t2": 7623.1224,
    "media_orgao_t2": 43224.1132,
    "minimo_orgao_t2": 432,
    "maximo_orgao_t2": 1324,
    "mediana_orgao_t2": 2242.3232
}
```

## Desarquivamentos

```
GET /dominio/desarquivamentos/<id_orgao>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
  {
    "numero_mprj": "123456789",
    "qtd_desarq": 1
  },
  {
    "numero_mprj": "987654321",
    "qtd_desarq": 2
  }
]
```

## Alertas

```
GET /dominio/alertas/<id_orgao>
```
a requisição aceita uma `querystring` opicional que diz o tipo de alerta desejado:

```
GET /dominio/alertas/<id_orgao>?tipo_alerta=MVVD
```

```
[
    {
        "sigla": "SIGLA 1",
        "descricao": "Descrição 1",
        "doc_dk": 12345678,
        "num_doc": "123456789",
        "num_ext": null,
        "etiqueta": "ETIQUETA 1",
        "classe_doc": "Classe Doc 1",
        "data_alerta": "2016-12-06T00:00:00Z",
        "orgao": 123456,
        "classe_hier": "CLASSE|HIERARQUIA",
        "dias_passados": -1
    },
    {
        "sigla": "SIGLA 2",
        "descricao": "Descrição 2",
        "doc_dk": 12345678,
        "num_doc": "123456789",
        "num_ext": null,
        "etiqueta": "ETIQUETA 2",
        "classe_doc": "Classe Doc 2",
        "data_alerta": "2016-12-06T00:00:00Z",
        "orgao": 123456,
        "classe_hier": "CLASSE|HIERARQUIA",
        "dias_passados": -1
    }
]
```

## Alertas de Compras fora do padrão

```
GET /dominio/alertas/compras/<id_orgao>
```

```
[
    {
        "sigla":"COMP",
        "contrato":"123456",
        "iditem":100000,
        "contrato_iditem":"123456",
        "item":"REAGENTE PREPARADO"
    },
    {
        "sigla":"COMP",
        "contrato":"89076",
        "iditem":200000,
        "contrato_iditem":"123456",
        "item":"LUVAS DESCARTÁVEIS"
    },
]
```

## Resumo dos Alertas

```
GET /dominio/alertas/list/<id_orgao>
```

```
[
 {
    'sigla': 'SIGLA 1',
    'descricao': 'DESC 1',
    'orgao': 0,
    'count': 10
 },
  {
    'sigla': 'SIGLA 2',
    'descricao': 'DESC 2',
    'orgao': 1,
    'count': 12
 },
]
```

## Lista Processos da Promotoria

```
GET /dominio/lista/processos/<id_orgao>?page=<int>

page: default=1
page_size (elementos por página): 20
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept


[
    {
        "id_orgao": 1,
        "classe_documento": "Ação Civil de Improbidade Administrativa",
        "docu_nr_mp": "1234",
        "docu_nr_externo": "5678",
        "docu_etiqueta": "ETIQUETA 1",
        "docu_personagens": "FULANO DE TAL, e outros...",
        "dt_ultimo_andamento": "2019-12-09T00:00:00",
        "ultimo_andamento": "Andamento 1",
        "url_tjrj": "http://www4.tjrj.jus.br/numeracaoUnica/faces/index.jsp?numProcesso=5678"
    },
    {
        "id_orgao": 1,
        "classe_documento": "Ação Civil de Improbidade Administrativa",
        "docu_nr_mp": "4321",
        "docu_nr_externo": "8765",
        "docu_etiqueta": null,
        "docu_personagens": "CICLANA DE TAL",
        "dt_ultimo_andamento": "2020-02-20T00:00:00",
        "ultimo_andamento": "Andamento 2",
        "url_tjrj": "http://www4.tjrj.jus.br/numeracaoUnica/faces/index.jsp?numProcesso=8765"
    }
]
```

## PIP

### Aproveitamentos PIP
```
GET /dominio/pip/aproveitamentos/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
  {
    "nr_aproveitamentos_periodo": 10,
    "variacao_periodo": 0.25,
    "top_n_pacote": [
        {"nm_promotoria": "Promotoria 1", "nr_aproveitamentos_periodo": 15},
        {"nm_promotoria": "Promotoria 2", "nr_aproveitamentos_periodo": 8},
    ],
    "nr_aisps": [1, 5],
    "top_n_aisp": [
        {"nm_promotoria": "Promotoria 3", "nr_aproveitamentos_periodo": 10},
        {"nm_promotoria": "Promotoria 2", "nr_aproveitamentos_periodo": 8},
    ],
    "tamanho_periodo_dias": 30,
  }
]
```

### Aberturas Mensais PIP
```
GET /dominio/pip/aberturas-mensal/<str:orgao_id>/<str:cpf>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "nr_aberturas_30_dias": 15,
    "nr_investigacoes_30_dias": 10
}
```

### Numero de Investigações AISP da PIP
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/pip/suamesa/investigacoes-aisp/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "aisp_nr_investigacoes": 34
}
```

### Numero de Inquéritos da PIP
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/pip/suamesa/inqueritos/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "pip_nr_inqueritos": 34
}
```

### Numero de PICs da PIP
(Será substituído pelo Sua Mesa Integrado!)
```
GET /dominio/pip/suamesa/pics/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "pip_nr_pics": 34
}
```

### Radar de Performance PIP
```
GET /dominio/pip/radar-performance/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "aisp_codigo": 16,
    "aisp_nome": "16",
    "orgao_id": 29933850,
    "nr_denuncias": 3,
    "nr_cautelares": 2,
    "nr_acordos_n_persecucao": 0,
    "nr_arquivamentos": 0,
    "nr_aberturas_vista": 12,
    "max_aisp_denuncias": 15,
    "max_aisp_cautelares": 6,
    "max_aisp_acordos": 0,
    "max_aisp_arquivamentos": 6,
    "max_aisp_aberturas_vista": 486,
    "perc_denuncias": 0.42857142857142855,
    "perc_cautelares": 0.3333333333333333,
    "perc_acordos": None,
    "perc_arquivamentos": 0.0,
    "perc_aberturas_vista": 0.030864197530864196,
    "med_aisp_denuncias": 3.0,
    "med_aisp_cautelares": 5.0,
    "med_aisp_acordos": 0.0,
    "med_aisp_arquivamentos": 0.0,
    "med_aisp_aberturas_vista": 79.0,
    "var_med_denuncias": 0.0,
    "var_med_cautelares": -0.6,
    "var_med_acordos": None,
    "var_med_arquivamentos": None,
    "var_med_aberturas_vista": -0.810126582278481,
    "dt_calculo": datetime(2020, 4, 22, 13, 36, 6, 668000),
    "nm_max_denuncias": "1ª Promotoria de Justiça",
    "nm_max_cautelares": "2ª Promotoria de Justiça",
    "nm_max_acordos": "3ª Promotoria de Justiça",
    "nm_max_arquivamentos": "4ª Promotoria de Justiça",
    "nm_max_abeturas_vista": "5ª Promotoria de Justiça",
}
```

### Principais Investigados da PIP
```
GET /dominio/pip/principais-investigados/<str:orgao_id>/<str:cpf>?page=<int>

page: default=1
page_size (elementos por página): 20
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "nm_investigado": "Nome2",
        "representante_dk": "1278",
        "pip_codigo": 1,
        "nr_investigacoes": 5,
        "flag_multipromotoria": True,
        "flag_top50": None,
        "is_pinned": True,
        "is_removed": False
    },
    {
        "nm_investigado": "Nome1",
        "representante_dk": "1234",
        "pip_codigo": 1,
        "nr_investigacoes": 10,
        "flag_multipromotoria": None,
        "flag_top50": True,
        "is_pinned": False,
        "is_removed": False
    },
]
```

```
POST /dominio/pip/principais-investigados/<str:orgao_id>/<str:cpf>?action=<str>&representante_dk=<int>

action pode ser 'remove', 'unremove', 'pin' ou 'unpin'.
```

```
HTTP 200 OK
Allow: POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{"status": "Success!"}
```

### Principais Investigados (Perfil) da PIP
```
GET /dominio/pip/principais-investigados-lista/<str:representante_dk>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "representante_dk": 16,
        "orgao_id": 123,
        "documento_nr_mp": "123456",
        "documento_dt_cadastro": '2020-04-22T13:36:06.668000Z',
        "documento_classe": "Classe",
        "nm_orgao": "5ª Promotoria de Justiça",
        "etiqueta": "Etiqueta",
        "assuntos": ["Assunto 1", "Assunto 2"]
    },
    {
        "representante_dk": 16,
        "orgao_id": 456,
        "documento_nr_mp": "124578",
        "documento_dt_cadastro": '2020-04-22T13:36:06.668000Z',
        "documento_classe": "Classe",
        "nm_orgao": "4ª Promotoria de Justiça",
        "etiqueta": "Etiqueta",
        "assuntos": ["Assunto 1"]
    },
]
```

### Indicadores de Sucesso da PIP
```
GET /dominio/pip/indicadores-sucesso/<str:orgao_id>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
       "orgao_id":12345,
       "indice":0.342684993409904,
       "tipo":"p_finalizacoes"
     },
     {
       "orgao_id":12345,
       "indice":0.3333333333333333,
       "tipo":"p_resolutividade"
      },
      {
       "orgao_id":12345,
       "indice":0.139710035774807,
       "tipo":"p_elucidacoes"
      }
]
```
