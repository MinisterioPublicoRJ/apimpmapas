SELECT 
    pess_dk,
    coautores,
    docu_nr_mp,
    orgi_nm_orgao,
    assuntos,
    fsdc_ds_fase,
    dt_ultimo_andamento,
    desc_ultimo_andamento,
    docu_nr_externo
FROM {schema}.tb_pip_investigados_procedimentos
WHERE representante_dk = :dk AND rep_last_digit = :digit
AND cod_pct IN :pcts
ORDER BY fsdc_ds_fase, dt_ultimo_andamento DESC, docu_nr_mp DESC