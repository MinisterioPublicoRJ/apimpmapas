SELECT
    docu_nr_mp as num_procedimento,
    coma.cmrc_nm_comarca as comarca
FROM
    {schema}.mcpr_documento docto
JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
WHERE docu_dk = :docu_dk
    AND docu_cldc_dk = 392 -- Apenas IC
