WITH procedimentos as (
SELECT
    docu_orgi_orga_dk_responsavel,
    docu_nr_mp,
    docu_dt_cadastro,
    docu_dk
FROM {schema}.mcpr_documento
WHERE docu_cldc_dk IN (51219, 51220, 51221, 51222, 51223, 392, 395)
    AND datediff(last_day(now()), docu_dt_cadastro) / 365.2425 > 1
    AND docu_dt_cancelamento IS NULL
    AND docu_fsdc_dk = 1
    AND NOT docu_tpst_dk = 11
    AND docu_orgi_orga_dk_responsavel = :id_orgao
),
base AS (SELECT
    docu_dk,
    orgi_nm_orgao AS nome_promotoria,
    docu_nr_mp AS num_procedimento,
    docu_dt_cadastro,
    coma.cmrc_nm_comarca as comarca,
    COALESCE(group_concat(distinct replace(replace(arvore_assunto.hierarquia, split_part(arvore_assunto.hierarquia, '>', 1), ''), '>', ''), ';'), '') AS ementa
FROM procedimentos procs
JOIN {schema}.orgi_foro_orgao ofo ON procs.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
LEFT JOIN {schema}.mcpr_assunto_documento assunto_docto ON  assunto_docto.asdo_docu_dk = procs.docu_dk
LEFT JOIN {schema_aux}.mmps_assunto_docto arvore_assunto ON asdo_assu_dk = id
INNER JOIN {schema_aux}.atualizacao_pj_pacote pacote
    ON procs.docu_orgi_orga_dk_responsavel = pacote.id_orgao
GROUP BY docu_dk, num_procedimento, nome_promotoria, docu_dt_cadastro, comarca
ORDER BY num_procedimento)
SELECT
    nome_promotoria,
    num_procedimento,
    docu_dt_cadastro,
    comarca,
    ementa,
    COALESCE(group_concat(distinct pessoadistinta.pess_nm_pessoa), '') AS investigados
from base
LEFT JOIN
    (SELECT pers_docu_dk, pess_nm_pessoa
    FROM {schema}.mcpr_personagem personagem
LEFT JOIN {schema}.mcpr_pessoa pessoa ON pessoa.pess_dk = personagem.pers_pess_dk
    AND pessoa.pess_nm_pessoa
        NOT rlike '(^MP$|MINIST[EÉ]RIO\\s+P[UÚ]BLICO|DEFENSORIA\\s+P[UÚ]BLICA.*|MINSTERIO PUBLICO|MPRJ|MINITÉRIO PÚBLICO|JUSTI[ÇC]A P[UÚ]BLICA)'
    WHERE  personagem.pers_tppe_dk IN (290, 7, 21, 317, 20, 14, 32, 345, 40, 5, 24)
    ) AS pessoadistinta ON docu_dk = pessoadistinta.pers_docu_dk
GROUP BY num_procedimento, nome_promotoria, docu_dt_cadastro, comarca, ementa
ORDER BY num_procedimento
