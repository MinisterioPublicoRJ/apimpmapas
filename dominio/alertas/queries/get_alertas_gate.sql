SELECT 
    alrt_key,
    alrt_sigla,
    alrt_orgi_orga_dk,
    alrt_docu_dk,
    alrt_docu_nr_mp,
    alrt_date_referencia,
    alrt_dias_referencia,
    alrt_itcn_dk
FROM {schema}.mmps_alertas_gate alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id