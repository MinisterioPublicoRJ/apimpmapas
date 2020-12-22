SELECT docu_dk
FROM {schema}.tb_documentos_arquivados
WHERE docu_orgi_orga_dk_responsavel in (:ids_orgaos)
