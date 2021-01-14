SELECT 
    alrt_key,
    alrt_sigla,
    alrt_orgi_orga_dk,
    abr1_nr_procedimentos,
    abr1_ano_mes
FROM {schema}.mmps_alertas_abr1 alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id