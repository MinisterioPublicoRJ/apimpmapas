SELECT 
    alrt_key,
    alrt_sigla,
    alrt_orgi_orga_dk,
    isps_municipio,
    isps_indicador,
    isps_ano_referencia
FROM {schema}.mmps_alertas_isps alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id