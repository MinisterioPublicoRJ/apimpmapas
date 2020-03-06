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
