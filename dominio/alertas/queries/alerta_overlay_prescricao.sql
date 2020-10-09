SELECT
    adpr_nome_delito,
    adpr_investigado_nm,
    adpr_max_pena,
    adpr_delitos_multiplicadores,
    adpr_fator_pena,
    adpr_max_pena_fatorado,
    adpr_dt_inicial_prescricao,
    adpr_dt_final_prescricao
FROM {schema}.mmps_alerta_detalhe_prcr
WHERE adpr_docu_dk = :docu_dk
