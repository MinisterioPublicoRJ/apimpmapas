WITH procedimentos as (
SELECT
    docu_orgi_orga_dk_responsavel,
    docu_nr_mp,
    docu_dt_cadastro,
    docu_dk,
    docu_tx_etiqueta
FROM {schema}.mcpr_documento
WHERE docu_cldc_dk IN (51219, 51220, 51221, 51222, 51223, 392, 395)
    AND datediff(now(), docu_dt_cadastro) / 365.2425 > 1
    AND docu_dt_cancelamento IS NULL
    AND docu_fsdc_dk = 1
    AND NOT docu_tpst_dk = 11
    AND (
        date_part('year', now()) = 2020 AND date_part('month', now()) = 11
        OR date_part('month', now()) = 10
    )
    AND docu_orgi_orga_dk_responsavel = :id_orgao
)
SELECT
    orgi_nm_orgao AS nome_promotoria,
    docu_nr_mp AS num_procedimento,
    docu_dt_cadastro,
    coma.cmrc_nm_comarca as comarca,
    datediff(now(), docu_dt_cadastro) / 365.2425 AS tempo_em_curso,
    COALESCE(procs.docu_tx_etiqueta, '') as objeto,
    COALESCE(group_concat(DISTINCT replace(replace(arvore_assunto.hierarquia, split_part(arvore_assunto.hierarquia, '>', 1), ''), '>', ''), ';'), '') AS ementa,
    COALESCE(group_concat(DISTINCT pessoa.pess_nm_pessoa), '') AS investigados
FROM procedimentos procs
JOIN {schema}.orgi_foro_orgao ofo ON procs.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
LEFT JOIN {schema}.mcpr_assunto_documento assunto_docto ON  assunto_docto.asdo_docu_dk = procs.docu_dk
LEFT JOIN {schema_aux}.mmps_assunto_docto arvore_assunto ON asdo_assu_dk = id
INNER JOIN {schema_aux}.atualizacao_pj_pacote pacote
    ON procs.docu_orgi_orga_dk_responsavel = pacote.id_orgao
LEFT JOIN {schema}.mcpr_personagem personagem ON docu_dk = pers_docu_dk
    AND personagem.pers_tppe_dk IN (290, 7, 21, 317, 20, 14, 32, 345, 40, 5, 24)
LEFT JOIN {schema}.mcpr_pessoa pessoa ON pessoa.pess_dk = personagem.pers_pess_dk
    AND pessoa.pess_nm_pessoa not rlike '(MP.*|MINIST[EÉ]RIO\\s+P[UÚ]BLICO.*|DEFENSORIA\\\\s\\+P[UÚ]BLICA.*|MINSTERIO PUBLICO|MPRJ|MINITÉRIO PÚBLICO)'
GROUP BY num_procedimento, nome_promotoria, docu_dt_cadastro, comarca, objeto
ORDER BY num_procedimento
