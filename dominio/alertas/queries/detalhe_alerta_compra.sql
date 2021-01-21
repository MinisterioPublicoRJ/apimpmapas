SELECT
    comp_contratacao,
    comp_dt_contratacao,
    comp_item,
    comp_var_perc
FROM {schema_alertas}.mmps_alertas_comp
WHERE alrt_key = :alerta_id
