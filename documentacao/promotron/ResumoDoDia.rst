Resumo Do Dia
=============

.. contents:: :local:

O primeiro componente é o Resumo do Dia. Nele, são realizados cálculos
para formar frases relativas ao status do dia atual.

.. figure:: figuras/resumo_do_dia.png

   Componente do Resumo do Dia

Cada frase corresponde a uma View no Backend (ou seja, cada frase pode
ser considerada um sub-componente), de forma que cada uma delas terá sua
própria seção.

Frase de Resolutividade
-----------------------

User Manual
~~~~~~~~~~~

Esta frase indica a porcentagem de promotorias de mesma atribuição que
tiveram menos saídas do que a promotoria sendo analisada, nos últimos 30
dias correntes.

O conceito de atribuição segue o que foi definido em :ref:`introducao-atribuicao`.

Já saídas são os andamentos finalizadores considerados como resolutivos.
Os andamentos definidos para este fim são os presentes na tabela
auxiliar :ref:`tabelas-auxiliares-tb-regra-negocio-saida`.

Utilizando as regras, o cálculo é feito então contabilizando:

-  Os andamentos com data (pcao_dt_andamento) nos últimos 30 dias;
-  Que não foram cancelados;
-  Cujos documentos não foram cancelados;
-  Que tenham atribuição definida na tabela :ref:`tabelas-auxiliares-atualizacao-pj-pacote`;
-  E que sejam dos tipos definidos na tabela :ref:`tabelas-auxiliares-tb-regra-negocio-saida` para
   o pacote do órgão em questão.

Esta contagem é então utilizada para fazer um Ranking com promotorias dentro da mesma atribuição, e saber a porcentagem de promotorias que tem contagem menor do que a promotoria que está sendo analisada.

Um exemplo de possível resultado do ranking é o seguinte:

+------------+------------------+---------+
| Promotoria | Número de Saídas | Ranking |
+============+==================+=========+
| A          | 0                | 0.0     |
+------------+------------------+---------+
| B          | 1                | 0.33    |
+------------+------------------+---------+
| C          | 1                | 0.33    |
+------------+------------------+---------+
| D          | 2                | 1.0     |
+------------+------------------+---------+

A promotoria A não tem número de saída maior do que nenhuma outra promotoria, portanto seu Ranking é 0%.

Já as promotorias B e C possuem número de saídas maior do que A. Ao calcular o Ranking para B, olhamos as promotorias A, C e D; destas, B tem número de saídas maior apenas do que A, ou seja, seu Ranking será :math:`1/3 = 0.33 = 33\%`. O mesmo acontece para C. Ou seja, ao fazer o Ranking para uma promotoria, ela não é levada em consideração - apenas as outras.

Por último, a promotoria D possui mais saídas do que todas as outras, portanto seu Ranking é de 100%.

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: TB_SAIDA
   Colunas: 
      saidas (int)
      id_orgao (int)
      cod_pct (int)
      percent_rank (double)
      dt_calculo (timestamp)

O processo no BDA consiste em realizar as contagens de andamentos utilizando as regras explicadas na seção anterior, e em seguida realizar um PERCENT_RANK para calcular o Ranking dentro de cada atribuição.

Em seguida, a tabela é salva no BDA. Uma coluna com a data de realização do último cálculo também é adicionada. Cada cálculo sobrescreve os resultados anteriores.

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tabela_saida.py.

!! Apesar da frase dizer últimos 30 dias, parece que o script de criação
da tabela atualmente considera últimos 60 dias.

View Backend
************

::

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

Nome da View: `SaidasView`_. 

O seu objetivo é basicamente acessar a tabela TB_SAIDA no BDA, filtrando o resultado pelo órgão que está sendo analisado, serializar os dados, e retornar o resultado na resposta.

.. _SaidasView: https://github.com/MinisterioPublicoRJ/apimpmapas/blob/develop/dominio/tutela/views.py#L176

Dependências
~~~~~~~~~~~~

-  :ref:`tabelas-auxiliares-atualizacao-pj-pacote`
-  :ref:`tabelas-auxiliares-tb-regra-negocio-saida`
-  Tabelas do MGP

Troubleshooting
~~~~~~~~~~~~~~~

-  A tabela está sendo gerada com dados? Se sim, ela possui dados para a
   promotoria que apresenta erro?
-  Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o
   problema pode ser na geração da tabela no BDA, ou dos dados usados
   para gerá-las. Caso haja dados e eles não estejam aparecendo
   corretamente, pode ser um problema no backend.
-  Caso a tabela esteja com problemas, a promotoria sendo analisada tem
   pacote de atribuição definido na tabela
   :ref:`tabelas-auxiliares-atualizacao-pj-pacote`?
-  Caso ela possua pacote de atribuição, existem regras de saídas
   definidas para o pacote dela na tabela
   :ref:`tabelas-auxiliares-tb-regra-negocio-saida`?
-  Caso o erro não seja na tabela, a View no backend está retornando os
   dados corretamente para esta ou outras promotorias?

Frase de Acervo
---------------

.. _user-manual-1:

User Manual
~~~~~~~~~~~

O objetivo desta frase é comparar o acervo de uma promotoria com o acervo de outras promotorias dentro da mesma atribuição, e dizer se ela possui um volume de documentos regular ou não.

Para isso, são contados os documentos ativos de determinadas classes, especificamente, as classes definidas na tabela auxiliar :ref:`tabelas-auxiliares-tb-regra-negocio-investigacao`. Isso é feito para todas as promotorias de mesma atribuição.

Em seguida, com esses números em mão, calcula-se um limite superior (``HOUT``) e inferior (``LOUT``) a partir do qual um dado volume não seria mais regular. Compara-se então o acervo da promotoria com estes limites para definir se ela está com um volume considerado regular ou não.

Por exemplo, digamos que em uma dada atribuição, os valores calculados para os limites sejam ``HOUT = 50`` e ``LOUT = 5``. Isto quer dizer que uma promotoria que tenha 30 documentos em seu acervo possui um volume regular. No entanto, uma outra promotoria que possua 55 documentos terá volume maior do que o que é considerado regular para sua atribuição.


.. _estrutura-do-código-1:

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: TB_DISTRIBUICAO
   Colunas: 
      cod_orgao (decimal(8,0))
      acervo (int)
      cod_atribuicao (int)
      minimo (int)
      maximo (int)
      media (double)
      primeiro_quartil (double)
      mediana (double)
      terceiro_quartil (double)
      iqr (double)
      lout (double)
      hout (double)
      dt_inclusao (timestamp)

O processo no BDA consiste em extrair o acervo das promotorias de cada atribuição, de acordo com as regras definidas em :ref:`tabelas-auxiliares-tb-regra-negocio-investigacao`, e fazer a contagem.

Em seguida, para calcular o ``LOUT`` e ``HOUT``, as seguintes etapas são realizadas:

- Calcula-se o valor do primeiro quartil (``1Q``) e terceiro quartil (``3Q``), dentro da mesma atribuição;
- Calcula-se o ``IQR`` (:math:`IQR = 3Q - 1Q`);
- Calcula-se :math:`LOUT = 1Q - 1.5*IQR`;
- Calcula-se :math:`HOUT = 3Q + 1.5*IQR`.

Em seguida, a tabela é salva no BDA. Uma coluna com a data de realização do último cálculo também é adicionada. Cada cálculo sobrescreve os resultados anteriores.

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tabela_distribuicao.py.


View Backend
************

::

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

Nome da View: `OutliersView`_. 

O seu objetivo é basicamente acessar a tabela TB_DISTRIBUICAO no BDA, filtrando o resultado pelo órgão que está sendo analisado, serializar os dados, e retornar o resultado na resposta.

.. _OutliersView: https://github.com/MinisterioPublicoRJ/apimpmapas/blob/develop/dominio/tutela/views.py#L116


.. _dependências-1:

Dependências
~~~~~~~~~~~~

-  ``{schema_exadata_aux}.tb_acervo`` !! Precisa de documentação
-  :ref:`tabelas-auxiliares-tb-regra-negocio-investigacao`

.. _troubleshooting-1:

Troubleshooting
~~~~~~~~~~~~~~~

-  A tabela está sendo gerada com dados? Se sim, ela possui dados para a
   promotoria que apresenta erro?
-  Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o
   problema pode ser na geração da tabela no BDA, ou dos dados usados
   para gerá-las. Caso haja dados e eles não estejam aparecendo
   corretamente, pode ser um problema no backend.
-  Se o problema estiver na geração da tabela, a promotoria sendo
   analisada tem acervo definido na tabela
   ``{schema_exadata_aux}.tb_acervo``?
-  Caso tenha acervo definido, este acervo está associado a algum pacote
   de atribuição, ou está como ``NULL``? Se estiver ``NULL``, verificar
   se a promotoria possui pacote definido na tabela
   :ref:`tabelas-auxiliares-atualizacao-pj-pacote`.
-  Caso os dados em ``{schema_exadata_aux}.tb_acervo`` estejam OK,
   existem regras de investigação definidas para o pacote dela na tabela
   :ref:`tabelas-auxiliares-tb-regra-negocio-investigacao`?
-  Caso o problema não seja na tabela, a View do backend está retornando
   dados para outras promotorias?

Frase de Entradas
-----------------

.. _user-manual-2:

User Manual
~~~~~~~~~~~

A última frase é relativa ao número de vistas abertas em um determinado dia, e indica se o número de vistas em um determinado dia está dentro ou fora de um padrão considerado regular. 

A ideia é muito parecida com a `Frase de Acervo <#frase-de-acervo>`__, mas ao invés de comparar acervo em relação a outras promotorias da mesma atribuição, comparam-se vistas abertas em relação ao histórico do promotor naquela promotoria.

!! Queremos comparar sempre dentro do mesmo CPF? Ou queremos comparar
com o órgão inteiro?

O cálculo é feito pegando as vistas que foram abertas em cada dia, nos últimos 60 dias, excluindo sábados e domingos. Não são consideradas as vistas relativas a documentos cancelados. Com isso, é possível calcular a partir de quantas vistas (ou de quão poucas vistas) um dia é muito diferente dos outros. Limites superior e inferior (``HOUT`` e ``LOUT``), como do caso do acervo.

Diferente das outras frases do Resumo do Dia, a Frase de Entradas não possui tabela de regras, já que todas as vistas são consideradas, independente da classe do documento ao qual elas se referem.

.. _estrutura-do-código-2:

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: TB_DIST_ENTRADAS
   Colunas: 
      nr_entradas_hoje (int)
      comb_orga_dk (int)
      comb_cpf (string)
      minimo (int)
      maximo (int)
      media (double)
      primeiro_quartil (double)
      mediana (double)
      terceiro_quartil (double)
      iqr (double)
      lout (double)
      hout (double)

O processo no BDA consiste em extrair o número de vistas abertas da promotoria sendo analisada nos últimos 60 dias, excluindo sábados e domingos, para documentos que não estão cancelados. Isso é feito para combinações de órgão e CPF para os quais foram abertas vistas no período de análise.

Em seguida, para calcular o ``LOUT`` e ``HOUT``, as seguintes etapas são realizadas:

- Calcula-se o valor do primeiro quartil (``1Q``) e terceiro quartil (``3Q``), dentro da mesma combinação de órgão e CPF;
- Calcula-se o ``IQR`` (:math:`IQR = 3Q - 1Q`);
- Calcula-se :math:`LOUT = 1Q - 1.5*IQR`;
- Calcula-se :math:`HOUT = 3Q + 1.5*IQR`.

Em seguida, a tabela é salva no BDA. Cada cálculo sobrescreve os resultados anteriores.

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tabela_dist_entradas.py.


View Backend
************

::

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

Nome da View: `EntradasView`_. 

O seu objetivo é basicamente acessar a tabela TB_DIST_ENTRADAS no BDA, filtrando o resultado pelo órgão e CPF que estão sendo analisados, serializar os dados, e retornar o resultado na resposta.

.. _EntradasView: https://github.com/MinisterioPublicoRJ/apimpmapas/blob/develop/dominio/tutela/views.py#L218

.. _dependências-2:

Dependências
~~~~~~~~~~~~

-  Tabelas do ``{schema_exadata}``.

.. _troubleshooting-2:

Troubleshooting
~~~~~~~~~~~~~~~

-  A tabela está sendo gerada com dados? Se sim, ela possui dados para a
   promotoria que apresenta erro?
-  Se a tabela estiver sem dados, ou sem dados para aquela promotoria, o
   problema pode ser na geração da tabela no BDA, ou dos dados usados
   para gerá-las. Caso haja dados e eles não estejam aparecendo
   corretamente, pode ser um problema no backend.
-  Se o problema estiver na geração da tabela, o promotor sendo
   analisado teve vistas abertas na promotoria selecionado nos últimos
   60 dias? Caso sim, pode ser um bug no script de geração da tabela.
-  Caso o problema não seja na tabela, a View do backend está retornando
   dados para outras promotorias?
