SELECT orgao_dk,
cldc_dk,
docu_nr_mp,
docu_nr_externo,
docu_tx_etiqueta,
personagens,
representante_dk,
dt_ultimo_andamento,
ultimo_andamento,
url_tjrj
FROM {schema}.tb_lista_processos
WHERE orgao_dk = :orgao_id
ORDER BY dt_ultimo_andamento DESC