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
GET dominio/outliers/<id_orgao>/<yyyy-MM-dd>
```

```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "cod_atribuicao": <int:cod_atribuicao>,
    "minimo": 112,
    "maximo": 290,
    "media": 171.4,
    "primeiro_quartil": 140.25,
    "mediana": 153.5,
    "terceiro_quartil": 182.5,
    "iqr": 42.25,
    "lout": 76.875,
    "hout": 245.875
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

### Vistas Abertas

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

## Tempo Tramitação

```
GET /dominio/tempo-tramitacao/<id_orgao>
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