SELECT
    docto.docu_nr_mp as num_procedimento,
    pacote.orgi_nm_orgao nome_promotoria,
    coma.cmrc_nm_comarca as comarca,
    CASE WHEN docu_tx_etiqueta IS NOT NULL
        THEN docu_tx_etiqueta
    ELSE
        ''
    END as objeto,
    group_concat(DISTINCT CAST(asdo_assu_dk AS string), ';') codigo_assunto,
    split_part(arvore_assunto.hierarquia, '>', 1) atribuicao,
    group_concat(DISTINCT replace(replace(arvore_assunto.hierarquia, split_part(arvore_assunto.hierarquia, '>', 1), ''), '>', ''), ';') ementa,
    group_concat(DISTINCT pessoa.pess_nm_pessoa) investigados
FROM
    exadata_dev.mcpr_documento docto
    JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
    JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
    JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
    JOIN {schema}.mcpr_assunto_documento assunto_docto ON  assunto_docto.asdo_docu_dk = docto.docu_dk
    JOIN {schema_aux}.mmps_assunto_docto arvore_assunto ON asdo_assu_dk = id
    JOIN {schema_aux}.atualizacao_pj_pacote pacote ON docto.docu_orgi_orga_dk_responsavel = pacote.id_orgao
    LEFT JOIN {schema}.mcpr_personagem personagem ON docu_dk = pers_docu_dk
    LEFT JOIN {schema}.mcpr_pessoa pessoa ON pessoa.pess_dk = personagem.pers_pess_dk
WHERE docto.docu_dk = :docu_dk
    AND personagem.pers_tppe_dk IN (290, 7, 21, 317, 20, 14, 32, 345, 40, 5, 24)
    AND pessoa.pess_nm_pessoa not rlike '(MP.*|MINIST[EÉ]RIO\\s+P[UÚ]BLICO.*|DEFENSORIA\\\\s\\+P[UÚ]BLICA.*|MINSTERIO PUBLICO|MPRJ|MINITÉRIO PÚBLICO)'
GROUP BY num_procedimento, nome_promotoria, comarca, objeto, atribuicao
