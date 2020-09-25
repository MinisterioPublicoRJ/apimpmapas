.. _tabelas-auxiliares-begin:

Tabelas auxiliares
==================

.. contents:: :local:

Algumas tabelas foram geradas para auxiliar em alguns dos cálculos. Elas
se encontram no schema ``EXADATA_AUX`` ou ``EXADATA_AUX_DEV``. Para
referenciar o uso destes schemas auxiliares será usada a notação
``{schema_exadata_aux}``. Enquanto que para os schemas dos dados
extraídos do MGP (``EXADATA`` ou ``EXADATA_DEV``), usaremos
``{schema_exadata}``.

Tabelas de Hierarquia
---------------------

Estas tabelas são tabelas criadas para auxiliar a encontrar as seguintes
hierarquias:

-  Classe de Documento: MMPS_CLASSE_DOCTO
-  Tipo de Andamento: MMPS_TP_ANDAMENTO
-  Assunto do Documento: MMPS_ASSUNTO_DOCTO

Um ``SELECT`` em qualquer uma delas será auto-explicativo, e servem
apenas para ajudar a tornar a compreensão/busca de regras de negócio
mais simples.

A criação destas tabelas se encontra em
``scripts-bda/extract_hierarchy/src/extractor.py``.

TB_ACERVO
---------

O objetivo desta tabela é guardar o histórico de documentos ativos em cada promotoria. Em teoria, este seria o papel da tabela :ref:`know-how-mgp-mcpr-historico-fase-doc`. No entanto, esta tabela parece apresentar algumas inconsistências. Por conta disso, foi decidido no início do projeto adotar uma postura de manter um histórico do acervo à parte, para que ele possa ser utilizado em cálculos que levam em conta a variação do acervo ao longo do tempo.

Ela possui as seguintes colunas:

-  ``cod_orgao`` (int): o código numérico do órgão.
-  ``cod_atribuicao`` (int): o código numérico do pacote de atribuição.
-  ``acervo`` (int): quantidade de acervo daquele determinado tipo.
-  ``tipo_acervo`` (int): a classe do documento - equivale ao ``cldc_dk`` do documento.
-  ``dt_inclusao`` (timestamp): a data de cálculo do acervo ativo.
-  ``dt_partition`` (string): a data em formato 'DDMMYYYY' usada para particionar os resultados da tabela.

São considerados apenas os documentos Em Andamento, e que não foram cancelados. O órgão em questão não precisa ter pacote de atribuição definido para que seu acervo seja guardado. Neste caso, o campo ``cod_atribuicao`` terá valor ``NULL``.

Os resultados desta tabela são guardados por partição (definida pelo campo ``dt_partition``), assim, ao longo de um mesmo dia, os resultados serão sobrescritos para aquele dia, mantendo o resto do histórico intacto.

.. _tabelas-auxiliares-atualizacao-pj-pacote:

ATUALIZACAO_PJ_PACOTE
---------------------

Tabela contendo os pacotes de atribuição de cada órgão. Ela possui as
seguintes colunas:

-  ``cod_pct`` (int): o código numérico relativo ao pacote.
-  ``pacote_atribuicao`` (str): o nome do pacote de atribuição.
-  ``id_orgao`` (int): o código numérico do órgão.
-  ``orgao_codamp`` (str): o nome do órgão em formato abreviado.
-  ``orgi_nm_orgao`` (str): o nome completo do órgão, tal qual aparece
   na tabela ORGI_ORGAO do MGP.

Um órgão pode possuir apenas um pacote de atribuição. No entanto, alguns
órgãos podem não ter pacote atribuido na tabela (como foi, inicialmente,
o caso das PIPs - para elas, foram criados códigos especialmente para
comportá-las).

As Tutelas Coletivas correspondem aos seguintes pacotes:

+---------+-------------------------------------------------------+
| cod_pct | pacote_atribuicao                                     |
+=========+=======================================================+
| 20      | Tutela Coletiva Ampla                                 |
+---------+-------------------------------------------------------+
| 21      | Tutela Coletiva Ampla sem Idoso ou com Idoso Residual |
+---------+-------------------------------------------------------+
| 22      | Tutela Coletiva Ampla sem Idoso e Saúde               |
+---------+-------------------------------------------------------+
| 23      | Tutela Coletiva - Cidadania e Consumidor              |
+---------+-------------------------------------------------------+
| 24      | Tutela Coletiva - Meio Ambiente e Consumidor          |
+---------+-------------------------------------------------------+
| 25      | Tutela Coletiva - Cidadania Ampla                     |
+---------+-------------------------------------------------------+
| 26      | Tutela Coletiva - Cidadania Pura                      |
+---------+-------------------------------------------------------+
| 27      | Tutela Coletiva - Consumidor                          |
+---------+-------------------------------------------------------+
| 28      | Tutela Coletiva - Meio Ambiente                       |
+---------+-------------------------------------------------------+
| 29      | Tutela Coletiva - Ordem Urbanística                   |
+---------+-------------------------------------------------------+
| 30      | Tutela Coletiva - Educação                            |
+---------+-------------------------------------------------------+
| 31      | Tutela Coletiva - Infância e Juventude                |
+---------+-------------------------------------------------------+
| 32      | Tutela Coletiva - Saúde                               |
+---------+-------------------------------------------------------+
| 33      | Tutela Coletiva - Sem Ranking Específico              |
+---------+-------------------------------------------------------+

Já as PIPs estão divididas da seguinte maneira:

+---------+--------------------------------+
| cod_pct | pacote_atribuicao              |
+=========+================================+
| 200     | PIPs Territoriais 1a CI        |
+---------+--------------------------------+
| 201     | PIPs Territoriais 2a CI        |
+---------+--------------------------------+
| 202     | PIPs Territoriais 3a CI        |
+---------+--------------------------------+
| 203     | PIPs Territoriais Interior     |
+---------+--------------------------------+
| 204     | PIPs Violência Doméstica 1a CI |
+---------+--------------------------------+
| 205     | PIPs Violência Doméstica 2a CI |
+---------+--------------------------------+
| 206     | PIPs Violência Doméstica 3a CI |
+---------+--------------------------------+
| 207     | PIPs Especializadas 1a CI      |
+---------+--------------------------------+
| 208     | PIPs Especializadas 2a CI      |
+---------+--------------------------------+
| 209     | PIPs Especializadas 3a CI      |
+---------+--------------------------------+

Isso inclui as seguintes PIPs: (++ Tabela abaixo desatualizada! As PIPs aqui abaixo representam apenas os pacotes 200, 201 e 202. As PIPs de outros pacotes ainda não foram inclusas nesta tabela. Atualização por vir.)

+-----------------------------------+-----------------------------------+
| orgi_orga_dk                      | orgi_nm_orgao                     |
+===================================+===================================+
| 29934004                          | 1ª PIP TERRITORIAL - BANGU /      |
|                                   | CAMPO GRANDE                      |
+-----------------------------------+-----------------------------------+
| 29926583                          | 1ª PIP TERRITORIAL - BOTAFOGO /   |
|                                   | COPACABANA                        |
+-----------------------------------+-----------------------------------+
| 29926805                          | 1ª PIP TERRITORIAL - CENTRO /     |
|                                   | ZONA PORTUÁRIA                    |
+-----------------------------------+-----------------------------------+
| 29933502                          | 1ª PIP TERRITORIAL - ILHA DO      |
|                                   | GOVERNADOR / BONSUCESSO           |
+-----------------------------------+-----------------------------------+
| 29933955                          | 1ª PIP TERRITORIAL - MADUREIRA /  |
|                                   | JACAREPAGUÁ                       |
+-----------------------------------+-----------------------------------+
| 29933418                          | 1ª PIP TERRITORIAL - MEIER /      |
|                                   | TIJUCA                            |
+-----------------------------------+-----------------------------------+
| 29933590                          | 1ª PIP TERRITORIAL - PENHA /      |
|                                   | IRAJÁ                             |
+-----------------------------------+-----------------------------------+
| 29934363                          | 1ª PIP TERRITORIAL - SANTA CRUZ   |
+-----------------------------------+-----------------------------------+
| 29934303                          | 1ª PIP TERRITORIAL - ZONA SUL /   |
|                                   | BARRA DA TIJUCA                   |
+-----------------------------------+-----------------------------------+
| 30069167                          | 1ª PIP TERRITORIAL - DUQUE DE     |
|                                   | CAXIAS                            |
+-----------------------------------+-----------------------------------+
| 30034384                          | 1ª PIP TERRITORIAL - NITERÓI      |
+-----------------------------------+-----------------------------------+
| 30069669                          | 1ª PIP TERRITORIAL - NOVA IGUAÇU  |
+-----------------------------------+-----------------------------------+
| 30061624                          | 1ª PIP TERRITORIAL - SÃO GONÇALO  |
+-----------------------------------+-----------------------------------+
| 29934012                          | 2ª PIP TERRITORIAL - BANGU E      |
|                                   | CAMPO GRANDE                      |
+-----------------------------------+-----------------------------------+
| 29926616                          | 2ª PIP TERRITORIAL - BOTAFOGO /   |
|                                   | COPACABANA                        |
+-----------------------------------+-----------------------------------+
| 29927047                          | 2ª PIP TERRITORIAL - CENTRO /     |
|                                   | ZONA PORTUÁRIA                    |
+-----------------------------------+-----------------------------------+
| 29933521                          | 2ª PIP TERRITORIAL - ILHA DO      |
|                                   | GOVERNADOR / BONSUCESSO           |
+-----------------------------------+-----------------------------------+
| 29933967                          | 2ª PIP TERRITORIAL - MADUREIRA /  |
|                                   | JACAREPAGUÁ                       |
+-----------------------------------+-----------------------------------+
| 29933469                          | 2ª PIP TERRITORIAL - MEIER /      |
|                                   | TIJUCA                            |
+-----------------------------------+-----------------------------------+
| 29933830                          | 2ª PIP TERRITORIAL - PENHA /      |
|                                   | IRAJÁ                             |
+-----------------------------------+-----------------------------------+
| 29934376                          | 2ª PIP TERRITORIAL - SANTA CRUZ   |
|                                   | DO NÚCLEO RIO DE JANEIRO          |
+-----------------------------------+-----------------------------------+
| 29934337                          | 2ª PIP TERRITORIAL DA ÁREA ZONA   |
|                                   | SUL E BARRA DA TIJUCA DO NÚCLEO   |
|                                   | RIO                               |
+-----------------------------------+-----------------------------------+
| 30069433                          | 2ª PIP TERRITORIAL - DUQUE DE     |
|                                   | CAXIAS                            |
+-----------------------------------+-----------------------------------+
| 30061094                          | 2ª PIP TERRITORIAL - NITERÓI      |
+-----------------------------------+-----------------------------------+
| 30069693                          | 2ª PIP TERRITORIAL - NOVA IGUAÇU  |
+-----------------------------------+-----------------------------------+
| 30061694                          | 2ª PIP TERRITORIAL - SÃO GONÇALO  |
+-----------------------------------+-----------------------------------+
| 29934277                          | 3ª PIP TERRITORIAL - BANGU /      |
|                                   | CAMPO GRANDE                      |
+-----------------------------------+-----------------------------------+
| 29933374                          | 3ª PIP TERRITORIAL - CENTRO /     |
|                                   | ZONA PORTUÁRIA                    |
+-----------------------------------+-----------------------------------+
| 29933988                          | 3ª PIP TERRITORIAL - MADUREIRA /  |
|                                   | JACAREPAGUÁ                       |
+-----------------------------------+-----------------------------------+
| 29933470                          | 3ª PIP TERRITORIAL - MEIER /      |
|                                   | TIJUCA                            |
+-----------------------------------+-----------------------------------+
| 29933850                          | 3ª PIP TERRITORIAL - PENHA /      |
|                                   | IRAJÁ                             |
+-----------------------------------+-----------------------------------+
| 30069453                          | 3ª PIP TERRITORIAL - DUQUE DE     |
|                                   | CAXIAS                            |
+-----------------------------------+-----------------------------------+
| 30069732                          | 3ª PIP TERRITORIAL - NOVA IGUAÇU  |
+-----------------------------------+-----------------------------------+
| 30061723                          | 3ª PIP TERRITORIAL - SÃO GONÇALO  |
+-----------------------------------+-----------------------------------+
| 29933490                          | 4ª PIP TERRITORIAL - MEIER /      |
|                                   | TIJUCA                            |
+-----------------------------------+-----------------------------------+
| 30069490                          | 4ª PIP TERRITORIAL - DUQUE DE     |
|                                   | CAXIAS                            |
+-----------------------------------+-----------------------------------+
| 30070041                          | 4ª PIP TERRITORIAL - NOVA IGUAÇU  |
+-----------------------------------+-----------------------------------+
| 30069516                          | 5ª PIP TERRITORIAL - DUQUE DE     |
|                                   | CAXIAS                            |
+-----------------------------------+-----------------------------------+

A lista com todos os pacotes disponíveis na tabela pode ser vista com a
seguinte query:

::

   SELECT DISTINCT cod_pct, pacote_atribuicao 
   FROM {schema_exadata_aux}.atualizacao_pj_pacote 
   ORDER BY cod_pct;

O script que cria o pacote auxiliar para as PIPs está presente em
``scripts-bda/robo_promotoria/src/atualizacao_pj_pacote.sql``.

.. _tabelas-auxiliares-tb-pip-aisp:

TB_PIP_AISP
-----------

Tabela contendo o mapeamento das PIPs às suas respectivas AISPs. Também
mapeia a PIP ao código antigo dela - se houver. Possui as seguintes colunas:

-  ``pip_codigo`` (int) : o código numérico do órgão.
-  ``aisp_codigo`` (int) : o código numérico da AISP. Corresponde ao
   número do batalhão.
-  ``aisp_nome`` (str) : o nome da AISP, correspondente ao batalhão.
-  ``pip_codigo_antigo`` (int) : o código numérico antigo do órgão.

O ``pip_codigo_antigo`` é necessário em alguns cálculos pois os órgãos
(no sistema do MGP) correspondentes às PIPs atuais só foram criados no
início de 2020. Porém, as PIPs em si já existiam, mas sob um código
antigo diferente. Assim, ao buscar dados mais antigos, é necessário
utilizar os dois códigos. A exceção a este caso são as PIPs Territoriais de Interior, que mantiveram os mesmos códigos.

++ Pode ser interessante aqui colocar uma tabela com cada órgão e a lista de AISPs associadas

O script de criação da tabela se encontra em
``scripts-bda/robo_promotoria/src/create_table_pip_aisp.sql``.

.. _tabelas-auxiliares-tb-pip-cisp:

TB_PIP_CISP
-----------

Tabela contendo o mapeamento das PIPs às suas respectivas CISPs.

-  ``pip_codigo`` (int) : o código numérico do órgão.
-  ``cisp_codigo`` (int) : o código numérico da CISP. Corresponde ao
   número da DP.
-  ``cisp_nome`` (str) : o nome da CISP, correspondente à DP.

Atualmente, as PIPs Especializadas não estão associadas a nenhuma CISP.

.. _tabelas-auxiliares-tb-regra-negocio-investigacao:

TB_REGRA_NEGOCIO_INVESTIGACAO
-----------------------------

Tabela contendo as regras do que constitui uma investigação para um
determinado pacote de atribuição. Colunas:

-  ``classe_documento`` (int) : o código da classe do documento. Liga à
   tabela MCPR_CLASSE_DOCTO_MP pela coluna ``cldc_dk``. Também pode
   ligar com a tabela auxiliar MMPS_CLASSE_DOCTO por meio da coluna
   ``id``, para obter a hierarquia da classe.
-  ``cod_atribuicao`` (int) : o código da atribuição. Liga à tabela
   auxiliar ATUALIZACAO_PJ_PACOTE por meio da coluna ``cod_pct``.

As classes de documentos utilizadas no momento são:

-  Tutelas Coletivas (pacotes 20 a 33 como mostrado para a tabela
   ATUALIZACAO_PJ_PACOTE):

+-----------------------------------+-----------------------------------+
| classe_documento                  | hierarquia                        |
+===================================+===================================+
| 395                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Preparatório    |
+-----------------------------------+-----------------------------------+
| 392                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Inquérito Civil              |
+-----------------------------------+-----------------------------------+
| 51223                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | tutela de interesses individuais  |
|                                   | indisponíveis                     |
+-----------------------------------+-----------------------------------+
| 51222                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | outras atividades não sujeitas a  |
|                                   | inquérito civil                   |
+-----------------------------------+-----------------------------------+
| 51220                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Políticas       |
|                                   | Públicas                          |
+-----------------------------------+-----------------------------------+
| 51221                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de TAC             |
+-----------------------------------+-----------------------------------+
| 51219                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Instituições    |
+-----------------------------------+-----------------------------------+

-  PIPs (pacotes 200 a 209):

+-----------------------------------+-----------------------------------+
| classe_documento                  | hierarquia                        |
+===================================+===================================+
| 3                                 | PROCESSO MILITAR > PROCESSO       |
|                                   | CRIMINAL > Procedimentos          |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial Militar                  |
+-----------------------------------+-----------------------------------+
| 494                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial                          |
+-----------------------------------+-----------------------------------+
| 590                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Procedimento    |
|                                   | Investigatório Criminal (PIC-MP)  |
+-----------------------------------+-----------------------------------+

Para visualizar a hierarquia das classes definidas para cada pacote de
atribuição, a seguinte query pode ser utilizada:

::

   SELECT cod_pct, classe_documento, hierarquia
   FROM {schema_exadata_aux}.tb_regra_negocio_investigacao
   JOIN {schema_exadata_aux}.mmps_classe_docto ON id = classe_documento
   ORDER BY cod_pct;

O script de criação da tabela TB_REGRA_NEGOCIO_INVSETIGACAO está em
``scripts-bda/robo_promotoria/src/create_tables_regra_negocio.sql``.

Além disso, caso queira adicionar e/ou modificar as regras existentes
para um dado conjunto de pacotes, é possível fazê-lo por meio da
seguinte query:

::

   INSERT INTO {schema_exadata_aux}.TB_REGRA_NEGOCIO_INVESTIGACAO PARTITION(cod_atribuicao)
   SELECT 
     cldc_dk as classe_documento,
     cod_pct as cod_atribuicao
   FROM {schema_exadata}.MCPR_CLASSE_DOCTO_MP
   CROSS JOIN (
     SELECT DISTINCT cod_pct 
     FROM {schema_exadata_aux}.ATUALIZACAO_PJ_PACOTE
   ) p
   WHERE cldc_dk IN (51219, 51220,...)
   AND cod_pct IN (20, 21, 22,...)

Onde:

-  ``cldc_dk`` corresponde às classes de documentos que quer adicionar.
-  ``cod_pct`` corresponde aos pacotes aos quais vocês quer associar as
   classes definidas.

É importante notar que essa tabela é particionada por
``cod_atribuicao``, ou seja, ao adicionar uma classe associada a um
determinado pacote, tudo o que havia associado ao pacote anteriormente é
sobrescrito. Assim, caso a intenção seja apenas adicionar uma nova
classe, é necessário especificar a nova classe e também todas as outras
que estavam associadas anteriormente.

.. _tabelas-auxiliares-tb-regra-negocio-processo:

TB_REGRA_NEGOCIO_PROCESSO
-------------------------

Tabela contendo as regras do que constitui um processo para um
determinado pacote de atribuição. As colunas são as mesmas da tabela
auxiliar TB_REGRA_NEGOCIO_INVESTIGACAO:

-  ``classe_documento`` (int) : o código da classe do documento.
-  ``cod_atribuicao`` (int) : o código da atribuição.

As classes de documentos que definem um processo só estão definidas para
Tutelas Coletivas, já que nenhum componente da PIP utiliza essas
informações. Assim, para as Tutelas temos:

+-----------------------------------+-----------------------------------+
| classe_documento                  | hierarquia                        |
+===================================+===================================+
| 323                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução Provisória em Autos      |
|                                   | Suplementares                     |
+-----------------------------------+-----------------------------------+
| 319                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução de Título Extrajudicial  |
+-----------------------------------+-----------------------------------+
| 320                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução de Termo de Ajuste de    |
|                                   | Conduta                           |
+-----------------------------------+-----------------------------------+
| 18                                | SUPREMO TRIBUNAL FEDERAL > Ação   |
|                                   | Rescisória                        |
+-----------------------------------+-----------------------------------+
| 126                               | SUPERIOR TRIBUNAL DE JUSTIÇA >    |
|                                   | Ação Rescisória                   |
+-----------------------------------+-----------------------------------+
| 127                               | SUPERIOR TRIBUNAL DE JUSTIÇA >    |
|                                   | Ação de Improbidade               |
|                                   | Administrativa                    |
+-----------------------------------+-----------------------------------+
| 159                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Especiais de        |
|                                   | Jurisdição Contenciosa > Ação     |
|                                   | Rescisória                        |
+-----------------------------------+-----------------------------------+
| 175                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil Coletiva  |
+-----------------------------------+-----------------------------------+
| 176                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil de        |
|                                   | Improbidade Administrativa        |
+-----------------------------------+-----------------------------------+
| 177                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil Pública   |
+-----------------------------------+-----------------------------------+
| 582                               | PROCESSO CRIMINAL > Execução      |
|                                   | Criminal > Execução Provisória    |
+-----------------------------------+-----------------------------------+
| 441                               | JUIZADOS DA INFÂNCIA E DA         |
|                                   | JUVENTUDE > Seção Cível >         |
|                                   | Processo de Conhecimento > Ação   |
|                                   | Civil Pública                     |
+-----------------------------------+-----------------------------------+
| 51205                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução de Título Extrajudicial  |
|                                   | contra a Fazenda Pública          |
+-----------------------------------+-----------------------------------+
| 51217                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução de Título Extrajudicial  |
+-----------------------------------+-----------------------------------+
| 51218                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução Extrajudicial de         |
|                                   | Alimentos                         |
+-----------------------------------+-----------------------------------+

Para visualizar a hierarquia das classes definidas para cada pacote de
atribuição, a seguinte query pode ser utilizada:

::

   SELECT cod_pct, classe_documento, hierarquia
   FROM {schema_exadata_aux}.tb_regra_negocio_processo
   JOIN {schema_exadata_aux}.mmps_classe_docto ON id = classe_documento
   ORDER BY cod_pct;

O script de criação da tabela TB_REGRA_NEGOCIO_PROCESSO está em
``scripts-bda/robo_promotoria/src/create_tables_regra_negocio.sql``.

Além disso, caso queira adicionar e/ou modificar as regras existentes
para um dado conjunto de pacotes, é possível fazê-lo por meio da
seguinte query:

::

   INSERT INTO {schema_exadata_aux}.TB_REGRA_NEGOCIO_PROCESSO PARTITION(cod_atribuicao)
   SELECT 
     cldc_dk as classe_documento,
     cod_pct as cod_atribuicao
   FROM {schema_exadata}.MCPR_CLASSE_DOCTO_MP
   CROSS JOIN (
     SELECT DISTINCT cod_pct 
     FROM {schema_exadata_aux}.ATUALIZACAO_PJ_PACOTE
   ) p
   WHERE cldc_dk IN (18, 126, 127,...)
   AND cod_pct IN (20, 21, 22, 23,...)

Onde:

-  ``cldc_dk`` corresponde às classes de documentos que quer adicionar.
-  ``cod_pct`` corresponde aos pacotes aos quais vocês quer associar as
   classes definidas.

Esta tabela, como a tabela de investigações, é particionada por
``cod_atribuicao``. Assim, caso a intenção seja apenas adicionar uma
nova classe, é necessário especificar a nova classe e também todas as
outras que estavam associadas anteriormente.

.. _tabelas-auxiliares-tb-regra-negocio-saida:

TB_REGRA_NEGOCIO_SAIDA:
-----------------------

Tabela contendo as regras de quais andamentos constituem saídas
eficientes para um determinado pacote de atribuição. Possui as seguintes
colunas:

-  ``tp_andamento`` (int) : o código do tipo do andamento. Liga à tabela
   MCPR_TP_ANDAMENTO do MGP, pela coluna ``tppr_dk``. Também liga à
   tabela auxiliar MMPS_TP_ANDAMENTO, pela coluna ``id``, para
   visualizar a hierarquia do andamento.
-  ``cod_atribuicao`` (int) : o código da atribuição.

Os andamentos considerados saídas eficientes estão definidos da seguinte
maneira:

-  Tutelas Coletivas

+-----------------------------------+-----------------------------------+
| tp_andamento                      | hierarquia                        |
+===================================+===================================+
| 6251                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Petição Inicial                   |
+-----------------------------------+-----------------------------------+
| 6326                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral com TAC                  |
+-----------------------------------+-----------------------------------+
| 6644                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Resolução da questão  |
+-----------------------------------+-----------------------------------+
| 6655                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Com   |
|                                   | TAC                               |
+-----------------------------------+-----------------------------------+
| 6657                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Resolução da questão        |
+-----------------------------------+-----------------------------------+

-  PIPs

+-----------------------------------+-----------------------------------+
| tp_andamento                      | hierarquia                        |
+===================================+===================================+
| 1201                              | Oferecimento de denúncia          |
+-----------------------------------+-----------------------------------+
| 1202                              | Oferecimento de denúncia com      |
|                                   | pedido de prisão                  |
+-----------------------------------+-----------------------------------+
| 6252                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia                          |
+-----------------------------------+-----------------------------------+
| 6253                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia > Escrita                |
+-----------------------------------+-----------------------------------+
| 6254                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia > Oral                   |
+-----------------------------------+-----------------------------------+
| 6361                              | MEMBRO > Proposta de transação    |
|                                   | penal                             |
+-----------------------------------+-----------------------------------+
| 6362                              | MEMBRO > Proposta de suspensão    |
|                                   | condicional do processo           |
+-----------------------------------+-----------------------------------+
| 6391                              | MEMBRO > Ciência > Suspensão do   |
|                                   | processo - Art. 366 CPP           |
+-----------------------------------+-----------------------------------+
| 7827                              | MEMBRO > Despacho > Acordo        |
|                                   | Extrajudicial                     |
+-----------------------------------+-----------------------------------+
| 7914                              | MEMBRO > Acordo de Não Persecução |
|                                   | Penal                             |
+-----------------------------------+-----------------------------------+
| 7917                              | MEMBRO > Acordo de Não Persecução |
|                                   | Penal > Pedido de homologação de  |
|                                   | acordo                            |
+-----------------------------------+-----------------------------------+
| 7928                              | MEMBRO > Ciência > Homologação de |
|                                   | Acordo de Não Persecução Penal    |
+-----------------------------------+-----------------------------------+
| 7868                              | MEMBRO > Colaboração Premiada     |
+-----------------------------------+-----------------------------------+
| 7883                              | MEMBRO > Acordo de Não Persecução |
|                                   | Penal > Celebração de acordo      |
+-----------------------------------+-----------------------------------+
| 7915                              | MEMBRO > Acordo de Não Persecução |
|                                   | Penal > Oferecimento de acordo    |
+-----------------------------------+-----------------------------------+
| 7922                              | MEMBRO > Manifestação > Pela      |
|                                   | extinção da punibilidade > Em     |
|                                   | razão do cumprimento do Acordo de |
|                                   | Não Persecução Penal              |
+-----------------------------------+-----------------------------------+


::

   SELECT cod_pct, tp_andamento, hierarquia
   FROM {schema_exadata_aux}.tb_regra_negocio_saida
   JOIN {schema_exadata_aux}.mmps_tp_andamento ON id = tp_andamento
   ORDER BY cod_pct;

O script de criação da tabela TB_REGRA_NEGOCIO_SAIDA está em
``scripts-bda/robo_promotoria/src/create_tables_regra_negocio.sql``.

Além disso, caso queira adicionar e/ou modificar as regras existentes
para um dado conjunto de pacotes, é possível fazê-lo por meio da
seguinte query:

::

   INSERT INTO {schema_exadata_aux}.TB_REGRA_NEGOCIO_SAIDA PARTITION(cod_atribuicao)
   SELECT 
     tppr_dk as tp_andamento,
     cod_pct as cod_atribuicao
   FROM {schema_exadata}.MCPR_TP_ANDAMENTO
   CROSS JOIN (
     SELECT DISTINCT cod_pct 
     FROM {schema_exadata_aux}.ATUALIZACAO_PJ_PACOTE
   ) p
   WHERE tppr_dk IN (18, 126, 127,...)
   AND cod_pct IN (20, 21, 22, 23,...)

Onde:

-  ``tppr_dk`` corresponde aos tipos de andamento que quer adicionar.
-  ``cod_pct`` corresponde aos pacotes aos quais vocês quer associar as
   classes definidas.

Esta tabela, como as outras, é particionada por ``cod_atribuicao``.
Assim, caso a intenção seja apenas adicionar um novo andamento, é
necessário especificar o novo andamento e também todos os outros que
estavam associados anteriormente.
