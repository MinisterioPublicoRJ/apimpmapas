SELECT 
    docto.docu_nr_mp as num_procedimento,
    docto.docu_dt_fato as data_fato,
    coma.cmrc_nm_comarca as comarca_tj,
    DATEDIFF(now(), docto.docu_dt_fato) as tempo_passado,
    group_concat(assu.assu_nm_assunto) as assunto_docto,
    group_concat(assu.assu_tx_dispositivo_legal) as lei_docto
FROM 
    {schema}.mcpr_documento docto
    LEFT JOIN {schema}.mcpr_assunto_documento asdo ON docto.docu_dk = asdo.asdo_docu_dk
    JOIN {schema}.mcpr_assunto assu ON asdo.asdo_assu_dk = assu.assu_dk
    JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
    JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
    JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
WHERE docto.docu_dk = :docu_dk
GROUP BY
    docto.docu_nr_mp, 
    docto.docu_dt_fato,
    coma.cmrc_nm_comarca,
    DATEDIFF(now(), docto.docu_dt_fato)