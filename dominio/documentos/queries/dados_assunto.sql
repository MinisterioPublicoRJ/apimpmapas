SELECT
	pena.nome_delito,
	pena.artigo_lei,
	pena.max_pena,
	pena.multiplicador
FROM {schema_aux}.tb_penas_assuntos pena
JOIN {schema}.mcpr_assunto_documento asdo ON pena.id = asdo.asdo_assu_dk
WHERE asdo.asdo_docu_dk = :docu_dk
    AND pena.max_pena IS NOT NULL --TODO: verificar se podemos excluir ou devemos preencher
