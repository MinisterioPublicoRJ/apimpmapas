SELECT 
    representante_dk,
    pess_nm_pessoa,
    tppe_descricao,
    pip_codigo,
    docu_nr_mp,
    docu_dt_cadastro,
    cldc_ds_classe,
    orgi_nm_orgao,
    docu_tx_etiqueta,
    assuntos,
    fsdc_ds_fase
FROM {schema}.tb_pip_investigados_procedimentos
WHERE representante_dk = :dk