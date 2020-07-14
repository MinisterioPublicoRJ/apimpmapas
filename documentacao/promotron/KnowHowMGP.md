Know-How de tabelas - colunas mais usadas:
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
