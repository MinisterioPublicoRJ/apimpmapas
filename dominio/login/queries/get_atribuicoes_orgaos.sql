SELECT pacote_atribuicao
FROM {schema}.atualizacao_pj_pacote
WHERE id_orgao in (:ids_orgaos)
