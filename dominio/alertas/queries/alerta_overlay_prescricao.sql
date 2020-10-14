SELECT
    adpr_nome_delito,
    adpr_investigado_nm,
    adpr_max_pena,
    adpr_delitos_multiplicadores,
    adpr_fator_pena,
    adpr_max_pena_fatorado,
    adpr_dt_inicial_prescricao,
    adpr_dt_final_prescricao,
    concat_ws(
        '_',
        cast(adpr_docu_dk as string),
        nvl(cast(cast(adpr_investigado_pess_dk as int) as string), ''),
        cast(adpr_id_assunto as string)
    ) as adpr_chave
FROM {schema}.mmps_alerta_detalhe_prcr
WHERE adpr_docu_dk = :docu_dk
