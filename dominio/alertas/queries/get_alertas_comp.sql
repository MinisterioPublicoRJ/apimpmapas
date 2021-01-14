SELECT 
    alrt_key,
    alrt_sigla,
    alrt_orgi_orga_dk,
    comp_contratacao,
    comp_item,
    comp_id_item,
    comp_contrato_iditem
FROM {schema}.mmps_alertas_comp alrt
WHERE alrt.alrt_orgi_orga_dk = :orgao_id