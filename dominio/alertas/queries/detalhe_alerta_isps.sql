SELECT
    alrt_classe_hierarquia,
    alrt_descricao
FROM {schema}.mmps_alertas
WHERE alrt_dk = :alerta_id
