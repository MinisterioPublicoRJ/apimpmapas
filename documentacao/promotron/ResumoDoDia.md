# Resumo Do Dia

O primeiro componente é o Resumo do Dia. Nele, são realizados cálculos para formar frases relativas ao status do dia atual.

![title](figuras/resumo_do_dia.png)

Cada frase corresponde a uma View no Backend (ou seja, cada frase pode ser considerada um sub-componente), de forma que cada uma delas terá sua própria seção.

## Frase de Resolutividade

### User Manual

Esta frase indica a porcentagem de promotorias de mesma atribuição que tiveram menos saídas do que a promotoria sendo analisada, nos últimos 30 dias correntes.

O conceito de <b>atribuição</b> segue o que foi definido no arquivo README.md. <font color="orange">++Ideal é não repetir informação, mas ter como referenciar facilmente.</font>

Já <b>saídas</b> são os andamentos finalizadores considerados como resolutivos. Os andamentos definidos para este fim são os presentes na tabela auxiliar TB_REGRA_NEGOCIO_SAIDA. <font color="orange">++ Se eu conseguir fazer uma referência ou um hyperlink para a seção desta tabela auxiliar seria ótimo. Procurar se tem como.</font>

Utilizando as regras, o cálculo é feito então contabilizando:

- Os andamentos com data (pcao_dt_andamento) nos últimos 30 dias;
- Que não foram cancelados;
- Cujos documentos não foram cancelados;
- E que sejam dos tipos definidos na tabela TB_REGRA_NEGOCIO_SAIDA para o pacote do órgão em questão.

Esta contagem é então utilizada para fazer um ranking com promotorias dentro da mesma atribuição, e saber a porcentagem de promotorias que tem contagem menor do que a promotoria que está sendo analisada.

### Estrutura do Código

```
GET /dominio/saidas/<id_orgao>

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "saidas": 2,
    "id_orgao": <int:id_orgao>,
    "cod_pct": 26,
    "percent_rank": 0.8888888888888888,
    "dt_calculo": "2020-02-11T16:27:09.273000Z"
}
```

Script criação BDA -> Tabela -> View Backend -> Front

O script de cálculo pode ser encontrado em `scripts-bda/robo_promotoria/src/tabela_saida.py`.
A tabela final gerada se chama `{schema_exadata_aux}.tb_saida`.
A view no backend que utiliza a tabela gerada é a `SaidasView` localizada em `apimpmapas/dominio/tutela/views.py`.

<font color="green">!! Apesar da frase dizer últimos 30 dias, parece que o script de criação da tabela atualmente considera últimos 60 dias.</font>

### Dependências

* `{schema_exadata_aux}.atualizacao_pj_pacote`
* `{schema_exadata_aux}.tb_regra_negocio_saida`
* Tabelas do `{schema_exadata}`

### Troubleshooting

* A tabela está sendo gerada com dados? Se sim, ela possui dados para a promotoria que apresenta erro?
* Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o problema pode ser na geração da tabela no BDA, ou dos dados usados para gerá-las. Caso haja dados e eles não estejam aparecendo corretamente, pode ser um problema no backend.
* Caso a tabela esteja com problemas, a promotoria sendo analisada tem pacote de atribuição definido na tabela `{schema_exadata_aux}.atualizacao_pj_pacote`?
* Caso ela possua pacote de atribuição, existem regras de saídas definidas para o pacote dela na tabela `{schema_exadata_aux}.tb_regra_negocio_saida`?
* Caso o erro não seja na tabela, a View no backend está retornando os dados corretamente para esta ou outras promotorias?

## Frase de Acervo

### User Manual

Esta frase pega o número de documentos ativos de determinadas classes para as promotorias dentro da mesma atribuição (no dia em que está sendo visto), e em seguida calcula um limite superior e inferior a partir do qual um dado volume não seria mais regular. Compara-se então o acervo da promotoria com estes limites para definir se ela está com um volume considerado regular ou não.

Como no caso da Frase de Resolutividade, as regras das classes de documentos têm uma tabela própria, estando localizadas na tabela auxiliar TB_REGRA_NEGOCIO_INVESTIGACAO.

### Estrutura do Código

```
GET dominio/outliers/<id_orgao>

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

Script criação BDA -> Tabela -> View Backend -> Front

O script de cálculo pode ser encontrado em `scripts-bda/robo_promotoria/src/tabela_distribuicao.py`.
A tabela final gerada se chama `{schema_exadata_aux}.tb_distribuicao`.
A view no backend que utiliza a tabela gerada é a `OutliersView` localizada em `apimpmapas/dominio/tutela/views.py`.

### Dependências

* `{schema_exadata_aux}.tb_acervo`
* `{schema_exadata_aux}.tb_regra_negocio_investigacao`

### Troubleshooting

* A tabela está sendo gerada com dados? Se sim, ela possui dados para a promotoria que apresenta erro?
* Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o problema pode ser na geração da tabela no BDA, ou dos dados usados para gerá-las. Caso haja dados e eles não estejam aparecendo corretamente, pode ser um problema no backend.
* Se o problema estiver na geração da tabela, a promotoria sendo analisada tem acervo definido na tabela `{schema_exadata_aux}.tb_acervo`?
* Caso tenha acervo definido, este acervo está associado a algum pacote de atribuição, ou está como `NULL`? Se estiver `NULL`, verificar se a promotoria possui pacote definido na tabela `{schema_exadata_aux}.atualizacao_pj_pacote`.
* Caso os dados em `{schema_exadata_aux}.tb_acervo` estejam OK, existem regras de investigação definidas para o pacote dela na tabela `{schema_exadata_aux}.tb_regra_negocio_investigacao`?
* Caso o problema não seja na tabela, a View do backend está retornando dados para outras promotorias?

## Frase de Entradas

### User Manual

A última frase é relativa ao número de vistas abertas em um determinado dia, e indica se o número de vistas em um determinado dia está dentro ou fora do padrão. A ideia é muito parecida com a [Frase de Acervo](#frase-de-acervo) (!! Teste de link), mas ao invés de comparar acervo em relação a outras promotorias da mesma atribuição, comparam-se vistas abertas em relação ao histórico do promotor naquela promotoria.<br>

<font color="green">!! Queremos comparar sempre dentro do mesmo CPF? Ou queremos comparar com o órgão inteiro?</font>

O cálculo é feito pegando as vistas que foram abertas em cada dia, nos últimos 60 dias, excluindo sábados e domingos. Também não são consideradas as vistas relativas a documentos cancelados. Com isso, é possível calcular a partir de quantas vistas (ou de quão poucas vistas) um dia é muito diferente dos outros. Limites superior e inferior, como do caso do acervo.
<font color="orange">++ Explicação pode melhorar, talvez com um desenho?</font>

Diferente das outras frases do Resumo do Dia, a Frase de Entradas não possui tabela de regras, já que todas as vistas são consideradas, independente da classe do documento ao qual elas se referem.

### Estrutura do Código

```
GET dominio/entradas/<str:orgao_id>/<str:nr_cpf>

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "nr_entradas_hoje": 10,
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

Script criação BDA -> Tabela -> View Backend -> Front

O script de cálculo pode ser encontrado em `scripts-bda/robo_promotoria/src/tabela_dist_entradas.py`.
A tabela final gerada se chama `{schema_exadata_aux}.tb_dist_entradas`.
A view no backend que utiliza a tabela gerada é a `EntradasView` localizada em `apimpmapas/dominio/tutela/views.py`.

### Dependências

* Tabelas do `{schema_exadata}`.

### Troubleshooting

* A tabela está sendo gerada com dados? Se sim, ela possui dados para a promotoria que apresenta erro?
* Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o problema pode ser na geração da tabela no BDA, ou dos dados usados para gerá-las. Caso haja dados e eles não estejam aparecendo corretamente, pode ser um problema no backend.
* Se o problema estiver na geração da tabela, o promotor sendo analisado teve vistas abertas na promotoria selecionado nos últimos 60 dias? Caso sim, pode ser um bug no script de geração da tabela.
* Caso o problema não seja na tabela, a View do backend está retornando dados para outras promotorias?
