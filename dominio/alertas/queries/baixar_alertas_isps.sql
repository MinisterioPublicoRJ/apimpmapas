SELECT 
    isps_indicador,
    isps_municipio
FROM {schema}.mmps_alertas_isps alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type