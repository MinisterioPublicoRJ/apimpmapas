SELECT t.*, CASE WHEN D.disp_alrt_key IS NULL AND DT.disp_alrt_key IS NULL THEN 0 ELSE 1 END AS flag_dispensado
FROM (
    SELECT 
        alrt_docu_dk,
        alrt_docu_nr_mp,
        alrt_date_referencia,
        alrt_orgi_orga_dk,
        alrt_dias_referencia,
        CASE WHEN alrt_sigla = 'GATE' THEN cast(alrt_dk_referencia as string) ELSE 'NO_ID' END as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_mgp alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        NULL as alrt_docu_dk,
        NULL as alrt_docu_nr_mp,
        NULL as alrt_date_referencia,
        alrt_orgi_orga_dk,
        NULL as alrt_dias_referencia,
        'NO_ID' as alrt_dk,
        alrt_sigla,
        isps_indicador as alrt_descricao,
        isps_municipio as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_isps alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        NULL as alrt_docu_dk,
        NULL as alrt_docu_nr_mp,
        NULL as alrt_date_referencia,
        alrt_orgi_orga_dk,
        abr1_nr_procedimentos as alrt_dias_referencia,
        'NO_ID' as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_abr1 alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
    UNION ALL
    SELECT 
        NULL as alrt_docu_dk,
        NULL as alrt_docu_nr_mp,
        NULL as alrt_date_referencia,
        alrt_orgi_orga_dk,
        ro_qt_ros_faltantes as alrt_dias_referencia,
        cast(ro_nr_delegacia as string) as alrt_dk,
        alrt_sigla,
        NULL as alrt_descricao,
        NULL as alrt_classe_hierarquia,
        NULL as alrt_docu_nr_externo,
        alrt_key
    FROM {schema}.mmps_alertas_ro alrt
    WHERE alrt.alrt_orgi_orga_dk = :orgao_id
) t
LEFT JOIN {schema}.hbase_dispensados D ON D.disp_alrt_key = alrt_key
LEFT JOIN {schema}.hbase_dispensados_todos DT ON DT.disp_alrt_key = regexp_replace(alrt_key, "\.[0-9]*$", '')