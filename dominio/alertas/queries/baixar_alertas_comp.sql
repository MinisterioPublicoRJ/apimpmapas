SELECT 
    comp_contratacao,
    comp_id_item,
    comp_item
FROM {schema}.mmps_alertas_comp alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id
AND alrt.alrt_sigla = :alrt_type