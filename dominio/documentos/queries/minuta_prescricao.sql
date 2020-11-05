SELECT
    docto.docu_nr_mp as num_procedimento,
    COALESCE(docto.docu_dt_fato, docto.docu_dt_cadastro) as data_fato,
    docto.docu_orgi_orga_dk_responsavel as orgao_responsavel,
    coma.cmrc_nm_comarca as comarca_tj,
    CAST(TRUNCATE((DATEDIFF(now(), COALESCE(docto.docu_dt_fato, docto.docu_dt_cadastro))/365)) AS string) as tempo_passado
FROM
    {schema}.mcpr_documento docto
    JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
    JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
    JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
WHERE docto.docu_dk = :docu_dk
