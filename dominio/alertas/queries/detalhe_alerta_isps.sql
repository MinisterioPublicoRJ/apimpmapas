SELECT
    alrt_municipio,
    alrt_indicador
FROM {schema}.mmps_alertas_isps
WHERE alrt_dk = :alerta_id
