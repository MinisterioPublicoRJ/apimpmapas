Know-How MGP
============

Know-How de tabelas MGP - colunas e dados mais usados:

Para se referir ao schema que guarda as tabelas vindas do MGP, iremos
utilizar a notação ``{schema_exadata}`` que diz respeito tanto ao scheme
``exadata`` quanto ``exadata_dev``.

MCPR_DOCUMENTO
--------------

-  ``docu_dk``: Chave primária da tabela de documentos.
-  ``docu_ano``: Ano do documento.
-  ``docu_nr_externo``: Número externo do documento, caso haja.
-  ``docu_nr_mp``: Número do documento no MP. Para um usuário comum,
   pode ser mais fácil identificar um documento pelo seu número no MP,
   do que por sua chave primária no banco.
-  ``docu_orgi_orga_dk_responsavel``: É o órgão responsável pelo
   documento. Liga com a tabela ``ORGI_ORGAO``.
-  ``docu_tpst_dk``: Usado para indicar a situação de um documento. Liga
   com a tabela ``MCPR_TP_SITUACAO_DOCUMENTO``.
-  ``docu_fsdc_dk``: Usado para indicar a fase do documento, liga com a
   tabela ``MCPR_FASES_DOCUMENTO``.
-  ``docu_cldc_dk``: É a classe do documento. Liga com
   ``MCPR_CLASSE_DOCTO_MP``. É possível também ligar com
   ``{schema_exadata_aux}.MMPS_CLASSE_DOCTO`` para pegar a hierarquia
   completa das classes. A classe do documento pode ser ``NULL``.
-  ``docu_dt_cadastro``: Data de cadastro do documento no sistema. Esta
   data não necessariamente bate com a data ou ano de criação do
   documento físico, e pode haver discrepâncias grandes para documentos
   mais antigos.

Para excluir os documentos que foram cancelados das queries:
``docu_tpst_dk != 11``. Para pegar apenas os documentos que ainda estão
em andamento: ``docu_fsdc_dk = 1``.

Os documentos possuem colunas de andamentos e tipos de andamentos
(``docu_pcao_dk`` e ``docu_tppr_dk``) que em teoria indicam o dk do
último andamento, e o tipo do último andamento. Mas não parecem ser
confiáveis sempre. Em um grande número de casos, a coluna
``docu_pcao_dk`` de fato parece bater com o ``pcao_dk`` do último
andamento. No caso do ``docu_tppr_dk`` isto é menos comum. Isso pode ser
verificado com ajuda da query seguinte (e modificando-a para analisar
pontos específicos):

::

   WITH DOCS_MAX_ANDAMENTO AS (
       SELECT docu_dk, docu_pcao_dk, docu_tppr_dk, pcao_dk, pcao_dt_andamento, stao_tppr_dk, MAX(pcao_dt_andamento) OVER(PARTITION BY docu_dk) as max_dt
       FROM exadata_dev.mcpr_documento
       JOIN exadata_dev.mcpr_vista ON vist_docu_dk = docu_dk
       JOIN exadata_dev.mcpr_andamento ON vist_dk = pcao_vist_dk
       JOIN exadata_dev.mcpr_sub_andamento ON stao_pcao_dk = pcao_dk
       JOIN exadata_aux_dev.atualizacao_pj_pacote ON id_orgao = docu_orgi_orga_dk_responsavel
       WHERE cod_pct IN (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 200)
   )
   SELECT COUNT(DISTINCT docu_dk) 
   FROM DOCS_MAX_ANDAMENTO
   WHERE max_dt = pcao_dt_andamento
   AND docu_pcao_dk != pcao_dk --OR docu_tppr_dk != stao_tppr_dk)
   AND docu_dk NOT IN (SELECT DISTINCT docu_dk FROM DOCS_MAX_ANDAMENTO WHERE max_dt = pcao_dt_andamento AND docu_pcao_dk = pcao_dk);

Não está clara a discrepância entre ``docu_tppr_dk`` e o ``tppr_dk`` do
``docu_pcao_dk`` correspondente. Às vezes parece ocorrer por meio de um
de-para. Por exemplo, em casos em que ``tppr_dk = 6002``, o
``docu_tppr_dk = 1001``, ambos descrevendo transformações de
Procedimentos Preparatórios em Inquérito Civil - porém com códigos
diferentes. Mas isso não é de forma alguma um padrão, já que muitas
vezes o ``docu_tppr_dk`` pode indicar algo completamente diferente, ou
mesmo ter valor ``NULL``.

MCPR_HISTORICO_FASE_DOC
-----------------------

A relação da tabela ``MCPR_DOCUMENTO`` com a tabela do histórico
``MCPR_HISTORICO_FASE_DOC`` parece ser mais confiável, embora também
possua discrepâncias. Para documentos mais antigos, essa tabela tem
erros muito maiores. Porém, quando olhamos documentos mais recentes, ela
possui uma confiabilidade maior. Ainda assim, existem erros nela.

Alguns andamentos finalizadores que estamos considerando, não são
considerados como finalizadores pela tabela de histórico. Da mesma
forma, alguns andamentos considerados como finalizadores nesta tabela,
não são finalizadores para nós. Isso causa discrepâncias entre a
contagem feita em componentes como o Finalizados do Sua Mesa, e a
contagem dada pela tabela de histórico:

::

   SELECT docu_orgi_orga_dk_responsavel, docu_dk, hcfs_dt_inicio, hcfs_dt_fim, hcfs_tppr_dk, hierarquia
   FROM exadata_dev.mcpr_historico_fase_doc
   JOIN exadata_dev.mcpr_documento ON docu_dk = hcfs_docu_dk
   JOIN exadata_aux_dev.atualizacao_pj_pacote ON id_orgao = docu_orgi_orga_dk_responsavel
   JOIN exadata_aux_dev.mmps_tp_andamento ON id = hcfs_tppr_dk
   WHERE cod_pct IN (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33)
   AND hcfs_fsdc_dk = 2
   AND hcfs_dt_inicio >= days_sub(current_timestamp(), 30)
   AND docu_tpst_dk != 11
   AND docu_orgi_orga_dk_responsavel = 400533;

Os ``hcfs_tppr_dk`` pelo menos batem com o ``tppr_dk`` dado pelo
``pcao_dk`` indicado no ``hcfs_pcao_dk`` da tabela. (Colocar uma query
aqui que mostre isso de forma mais clara).

MCPR_VISTA
----------

-  ``vist_dk``: Chave primária das vistas. Pode ser negativa.
-  ``vist_docu_dk``: Chave estrangeira usada para ligar a vista ao seu
   documento, na tabela ``MCPR_DOCUMENTO``. Não pode ser ``NULL``.
-  ``vist_orgi_orga_dk``: órgão para o qual a vista foi aberta. Liga com
   a tabela ``ORGI_ORGAO``.
-  ``vist_dt_abertura_vista``: Data de abertura da vista.
-  ``vist_dt_fechamento_vista``: Data de fechamento da vista.
-  ``vist_pesf_pess_dk_resp_andam``: A pessoa fisica para a qual a vista
   foi aberta. Liga com a tabela ``MCPR_PESSOA_FISICA``.

Vistas podem não ter andamentos associados ainda. De forma que, em
determinadas situações, é necessário realizar a junção entre tabelas por
meio de um ``LEFT JOIN``.

Por exemplo, caso queiramos fazer uma análise da porcentagem de vistas
em um determinado período que levaram a um determinado tipo de
andamento, precisamos juntar as tabelas com um ``LEFT JOIN`` para não
tirar as vistas que não possuem andamentos ainda.

Alguns outros pontos:

-  Documentos cancelados podem ter vistas abertas depois da data de
   cancelamento:

::

   SELECT *
   FROM exadata_dev.mcpr_documento
   JOIN exadata_dev.mcpr_vista ON vist_docu_dk = docu_dk
   WHERE docu_tpst_dk = 11
   AND docu_dt_cancelamento < vist_dt_abertura_vista;

-  O sistema permite que a data de abertura de vista seja feita no
   futuro:

::

   SELECT *
   FROM exadata_dev.mcpr_vista
   WHERE vist_dt_abertura_vista > current_timestamp();

-  Há, também, casos de vistas no sistema que tem data de fechamento
   anterior à data de abertura:

::

   SELECT *
   FROM exadata_dev.mcpr_vista
   WHERE to_date(vist_dt_abertura_vista) > to_date(vist_dt_fechamento_vista);

MCPR_ANDAMENTO
--------------

-  ``pcao_dk``: Chave primária dos andamentos. Pode ser negativa.
-  ``pcao_vist_dk``: Chave usada para ligar o andamento à vista, na
   tabela ``MCPR_VISTA``. Não pode ser ``NULL``.
-  ``pcao_dt_andamento``: Data em que o andamento foi realizado.
-  ``pcao_dt_cancelamento``: Data em que o andamento foi cancelado, caso
   tenha sido - senão, é ``NULL``.
-  ``year_month``: Coluna usada exclusivamente no BDA para particionar a
   tabela de andamentos, no formato ``YYYYMM``. Se possível, ao utilizar
   esta tabela, fazer o filtro de data usando esta coluna, mesmo que
   parcialmente.

Uma vista pode estar ligada a mais de um andamento.

Pode ocorrer de um andamento não ter sub-andamento, mas são pouquíssimos
casos (3406 casos da última vez que a query foi executada):

::

   SELECT COUNT(DISTINCT pcao_dk)
   FROM exadata_dev.mcpr_andamento
   WHERE pcao_dk NOT IN (SELECT DISTINCT stao_pcao_dk FROM exadata_dev.mcpr_sub_andamento);

MCPR_SUB_ANDAMENTO
------------------

-  ``stao_dk``: Chave primária dos sub-andamentos. Pode ser negativa.
-  ``stao_pcao_dk``: Chave usada para ligar o sub-andamento ao seu
   andamento, na tabela ``MCPR_ANDAMENTO``. Não pode ser ``NULL``.
-  ``stao_tppr_dk``: O tipo de andamento. Liga com
   ``MCPR_TP_ANDAMENTO``. Também pode ligar com
   ``{schema_exadata_aux}.MMPS_TP_ANDAMENTO`` para pegar a hierarquia.
   Não pode ser ``NULL``.

Um andamento pode ter mais de um sub-andamento.

MCPR_TP_SITUACAO_DOCUMENTO
--------------------------

Tabela que enumera os tipos de situação de documento existentes no
banco. Liga no ``docu_tpst_dk`` da tabela ``MCPR_DOCUMENTO``.

+---------+-------------------------------------+
| tpst_dk | tpst_ds_tp_situacao                 |
+=========+=====================================+
| 1       | Em Carga                            |
+---------+-------------------------------------+
| 2       | Em Trânsito                         |
+---------+-------------------------------------+
| 3       | Fora da Instituição                 |
+---------+-------------------------------------+
| 4       | Pendente de Complementação de Dados |
+---------+-------------------------------------+
| 5       | Disponível para Envio               |
+---------+-------------------------------------+
| 6       | Compondo Guia de Remessa            |
+---------+-------------------------------------+
| 7       | Esperando Movimento                 |
+---------+-------------------------------------+
| 9       | Em Arquivo                          |
+---------+-------------------------------------+
| 11      | Em análise/cancelado                |
+---------+-------------------------------------+
| 15      | Aguardando entrada/recebimento      |
+---------+-------------------------------------+

MCPR_FASES_DOCUMENTO
--------------------

Tabela que enumera os tipos de fase do documento existentes no banco.
Liga no ``docu_fsdc_dk`` da tabela ``MCPR_DOCUMENTO``.

+---------+--------------+
| fsdc_dk | fsdc_ds_fase |
+=========+==============+
| 1       | Em Andamento |
+---------+--------------+
| 2       | Finalizado   |
+---------+--------------+
