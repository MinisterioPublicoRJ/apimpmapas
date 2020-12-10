WITH pessoas_investigadas AS (
    SELECT pers.pers_docu_dk,
		   group_concat(DISTINCT pess_nm_pessoa) as nomes
    FROM {schema}.mcpr_pessoa pessoa
		JOIN {schema}.mcpr_personagem pers ON pessoa.pess_dk = pers.pers_pess_dk
    WHERE pers_docu_dk = :docu_dk
		AND pers.pers_tppe_dk IN (290, 7, 21, 317, 20, 14, 32, 345, 40, 5, 24)
		AND pessoa.pess_nm_pessoa not rlike '(MP.*|MINIST[EÉ]RIO\\s+P[UÚ]BLICO.*|DEFENSORIA\\\\s\\+P[UÚ]BLICA.*|MINSTERIO PUBLICO|MPRJ|MINITÉRIO PÚBLICO)'
    GROUP BY pers.pers_docu_dk
),
tipos_assuntos AS (
 SELECT asdo_docu_dk,
		GROUP_CONCAT(CAST(asdo_assu_dk AS STRING), ';') AS assuntos
	    FROM {schema}.mcpr_assunto_documento
    WHERE asdo_docu_dk = :docu_dk
    GROUP BY asdo_docu_dk
)
SELECT
    docto.docu_nr_mp as num_procedimento,
    pacote.orgi_nm_orgao nome_promotoria,
    coma.cmrc_nm_comarca as comarca,
    COALESCE(docu_tx_etiqueta, '') as objeto,
    COALESCE(t_assunt.assuntos, '') AS codigo_assunto,
    COALESCE(split_part(arvore_assunto.hierarquia, '>', 1), '') AS atribuicao,
    COALESCE(group_concat(DISTINCT replace(replace(arvore_assunto.hierarquia, split_part(arvore_assunto.hierarquia, '>', 1), ''), '>', ''), ';'), '') AS ementa,
    COALESCE(p_invest.nomes, '') AS investigados
FROM
    {schema}.mcpr_documento docto
    JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
    JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
    JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
    LEFT JOIN {schema}.mcpr_assunto_documento assunto_docto ON  assunto_docto.asdo_docu_dk = docto.docu_dk
    LEFT JOIN {schema_aux}.mmps_assunto_docto arvore_assunto ON asdo_assu_dk = id
    JOIN exadata_aux.atualizacao_pj_pacote pacote ON docto.docu_orgi_orga_dk_responsavel = pacote.id_orgao
    LEFT JOIN pessoas_investigadas p_invest ON docto.docu_dk = p_invest.pers_docu_dk
    LEFT JOIN tipos_assuntos t_assunt ON t_assunt.asdo_docu_dk = docto.docu_dk
WHERE docto.docu_dk = :docu_dk
GROUP BY num_procedimento, nome_promotoria, comarca, objeto, atribuicao, p_invest.nomes, t_assunt.assuntos
