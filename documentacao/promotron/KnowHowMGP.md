Know-How de tabelas - colunas mais usadas:
EXADATA_DEV

MCPR_DOCUMENTO:
docu_orgi_orga_dk - É o órgão responsável pelo documento. Uma vista pode ser aberta em um órgão relativa a um documento de outro órgão. Linka na tabela orgi_orgao
docu_tpst_dk - Usado para indicar se um documento está cancelado - docu_tpst_dk != 11 filtra os documentos não-cancelados
docu_fsdc_dk - Usado para indicar a fase do documento, liga com a tabela mcpr_fases_documento. 1 = Em Andamento, 2 = Finalizado
docu_cldc_dk - É a classe do documento. Liga com mcpr_classe_docto_mp. É possível também ligar com exadata_aux_dev.mmps_classe_docto para pegar a hierarquia completa das classes. A classe do documento pode ser NULL.

Documentos cancelados podem ter vistas abertas depois da data de cancelamento:

```
SELECT *
FROM exadata_dev.mcpr_documento
JOIN exadata_dev.mcpr_vista ON vist_docu_dk = docu_dk
WHERE docu_tpst_dk = 11
AND docu_dt_cancelamento < vist_dt_abertura_vista;
```

Os documentos possuem colunas de andamentos e tipos de andamentos (`docu_pcao_dk` e `docu_tppr_dk`) que em teoria indicam o dk do último andamento, e o tipo do último andamento. Mas não parecem ser confiáveis sempre. Em um grande número de casos, a coluna `docu_pcao_dk` de fato parece bater com o `pcao_dk` do último andamento. No caso do `docu_tppr_dk` isto é menos comum. Isso pode ser verificado com ajuda da query seguinte (e modificando-a para analisar pontos específicos):

```
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
```

Não está clara a discrepância entre `docu_tppr_dk` e o `tppr_dk` do `docu_pcao_dk` correspondente. Às vezes parece ocorrer por meio de um de-para. Por exemplo, em casos em que `tppr_dk = 6002`, o `docu_tppr_dk = 1001`, ambos descrevendo transformações de Procedimentos Preparatórios em Inquérito Civil - porém com códigos diferentes. Mas isso não é de forma alguma um padrão, já que muitas vezes o `docu_tppr_dk` pode indicar algo completamente diferente, ou mesmo ter valor `NULL`.

MCPR_HISTORICO_FASE_DOC

Já a relação com a tabela do histórico `{schema_exadata}.MCPR_HISTORICO_FASE_DOC` parece ser mais confiável, embora também possua discrepâncias. Para documentos mais antigos, essa tabela tem erros muito maiores. Porém, quando olhamos documentos mais recentes, ela possui uma confiabilidade maior. Ainda assim, existem erros nela. Alguns andamentos finalizadores que estamos considerando, não são considerados como finalizadores pela tabela de histórico. Da mesma forma, alguns andamentos considerados como finalizadores nesta tabela, não são finalizadores para nós. Isso causa discrepâncias entre a contagem feita no Sua Mesa, e a contagem dada pela tabela de histórico:

```
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

```

Os `hcfs_tppr_dk` pelo menos batem com o `tppr_dk` dado pelo `pcao_dk` indicado no `hcfs_pcao_dk` da tabela. (Colocar uma query aqui que mostre isso de forma mais clara).

MCPR_VISTA:
vist_docu_dk - Chave usada para ligar a vista ao seu documento, na tabela mcpr_documento
vist_orgi_orga_dk - órgão para o qual a vista foi aberta. Linka com a tabela orgi_orgao
vist_dt_abertura_vista - Data de abertura da vista. Em alguns casos parece que a data de abertura pode ser feita no futuro.
vist_dt_fechamento_vista - Data de fechamento da vista.
vist_pesf_pess_dk_resp_andam - A pessoa fisica para a qual a vista foi aberta. Linka com a tabela mcpr_pessoa_fisica

MCPR_ANDAMENTO:

pcao_dk - Chave primária, pode ser negativo??? Aparentemente sim
pcao_vist_dk - Chave usada para ligar o andamento à vista, na tabela mcpr_vista
pcao_dt_andamento - Data em que o andamento foi realizado.
pcao_dt_cancelamento - Data em que o andamento foi cancelado, caso tenha sido
year_month - coluna usada no BDA para particionar a tabela de andamentos, no formato YYYYMM. Se possível fazer o filtro de data usando esta coluna, mesmo parcialmente.

Um andamento pode ter vários sub-andamentos.

MCPR_SUB_ANDAMENTO:
stao_pcao_dk - Chave usada para ligar o subandamento ao seu andamento, na tabela mcpr_andamento
stao_tppr_dk - O tipo de andamento. Liga com mcpr_tp_andamento. Também pode ligar com exadata_aux_dev.mmps_tp_andamento para pegar a hierarquia.

-- perguntas: uma vista com vários andamentos? Vistas sem andamentos? Andamentos sem subandamentos ou sem vistas? Subandamento sem tipo?
-- Basicamente, qual a relação entre tabelas, e quais colunas podem vir nulas? Descobrir isso melhor (e guardar as queries pra documentação)Know-How de tabelas - colunas mais usadas:
EXADATA_DEV

MCPR_DOCUMENTO:
docu_orgi_orga_dk - É o órgão responsável pelo documento. Uma vista pode ser aberta em um órgão relativa a um documento de outro órgão. Linka na tabela orgi_orgao
docu_tpst_dk - Usado para indicar se um documento está cancelado - docu_tpst_dk != 11 filtra os documentos não-cancelados
docu_fsdc_dk - Usado para indicar a fase do documento, liga com a tabela mcpr_fases_documento. 1 = Em Andamento, 2 = Finalizado
docu_cldc_dk - É a classe do documento. Liga com mcpr_classe_docto_mp. É possível também ligar com exadata_aux_dev.mmps_classe_docto para pegar a hierarquia completa das classes.

MCPR_VISTA:
vist_docu_dk - Chave usada para ligar a vista ao seu documento, na tabela mcpr_documento
vist_orgi_orga_dk - órgão para o qual a vista foi aberta. Linka com a tabela orgi_orgao
vist_dt_abertura_vista - Data de abertura da vista. Em alguns casos parece que a data de abertura pode ser feita no futuro.
vist_dt_fechamento_vista - Data de fechamento da vista.
vist_pesf_pess_dk_resp_andam - A pessoa fisica para a qual a vista foi aberta. Linka com a tabela mcpr_pessoa_fisica

MCPR_ANDAMENTO:
pcao_vist_dk - Chave usada para ligar o andamento à vista, na tabela mcpr_vista
pcao_dt_andamento - Data em que o andamento foi realizado.
pcao_dt_cancelamento - Data em que o andamento foi cancelado, caso tenha sido
year_month - coluna usada no BDA para particionar a tabela de andamentos, no formato YYYYMM. Se possível fazer o filtro de data usando esta coluna, mesmo parcialmente.

MCPR_SUB_ANDAMENTO:
stao_pcao_dk - Chave usada para ligar o subandamento ao seu andamento, na tabela mcpr_andamento
stao_tppr_dk - O tipo de andamento. Liga com mcpr_tp_andamento. Também pode ligar com exadata_aux_dev.mmps_tp_andamento para pegar a hierarquia.

-- perguntas: uma vista com vários andamentos? Vistas sem andamentos? Andamentos sem subandamentos ou sem vistas? Subandamento sem tipo?
-- Basicamente, qual a relação entre tabelas (um pra um, um pra muitos, muitos pra muitos), quais colunas podem vir nulas, e algumas relações entre colunas que podem ser interessantes de anotar? (guardar as queries pra documentação que permitam verificar essas relações)
