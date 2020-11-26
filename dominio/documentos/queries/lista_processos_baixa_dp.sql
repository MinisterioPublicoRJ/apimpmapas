---Query temporária enquanto tabela auxiliar do alerta não é criada
WITH DOC_MOV AS (SELECT docu_dk,
    docu_nr_mp,
    docu_orgi_orga_dk_responsavel,
    docu_nr_externo,
    movi_orga_dk_destino,
    COALESCE(mov.movi_dt_recebimento_guia, mov.movi_dt_envio_guia, mov.movi_dt_criacao_guia) AS dt_guia_pre
FROM {schema}.mcpr_documento doc
    JOIN {schema}.mcpr_item_movimentacao item_mov ON doc.docu_dk = item_mov.item_docu_dk
    JOIN {schema}.mcpr_movimentacao mov ON item_mov.item_movi_dk = mov.movi_dk
WHERE doc.docu_tpst_dk = 3 AND doc.docu_fsdc_dk = 1 AND docu_orgi_orga_dk_responsavel = :orgao_id
),
LAST_MOV AS (
    SELECT docu_dk, docu_nr_mp, docu_orgi_orga_dk_responsavel, max(dt_guia_pre) as ultima_data
    FROM DOC_MOV GROUP BY docu_dk, docu_nr_mp, docu_orgi_orga_dk_responsavel
)
SELECT DOC_MOV.docu_nr_mp,
    orge_nm_orgao,
    LAST_MOV.ultima_data
    FROM LAST_MOV
    JOIN DOC_MOV ON DOC_MOV.docu_dk = LAST_MOV.docu_dk AND DOC_MOV.dt_guia_pre = LAST_MOV.ultima_data
    JOIN {schema}.mprj_orgao_ext orgao_ext ON orgao_ext.orge_orga_dk = movi_orga_dk_destino AND orge_tpoe_dk IN (54, 60, 61, 68)
