SELECT
    docto.docu_nr_mp as num_procedimento,
    pacote.orgi_nm_orgao nome_promotoria,
    coma.cmrc_nm_comarca as comarca,
    docu_tx_etiqueta objeto,
    asdo_assu_dk codigo_assunto,
    split_part(arvore_assunto.hierarquia, '>', 1) atribuicao,
    replace(replace(arvore_assunto.hierarquia, split_part(arvore_assunto.hierarquia, '>', 1), ''), '>', '') ementa
FROM
    exadata_dev.mcpr_documento docto
    JOIN {schema}.orgi_foro_orgao ofo ON docto.docu_orgi_orga_dk_responsavel = ofo.forg_orgi_dk
    JOIN {schema}.orgi_foro foro ON foro.cofo_dk = ofo.forg_cofo_dk
    JOIN {schema}.orgi_comarca coma ON foro.cofo_cmrc_dk = coma.cmrc_dk
    JOIN {schema}.mcpr_assunto_documento assunto_docto ON  assunto_docto.asdo_docu_dk = docto.docu_dk
    JOIN {schema_aux}.mmps_assunto_docto arvore_assunto ON asdo_assu_dk = id
    JOIN {schema_aux}.atualizacao_pj_pacote pacote ON docto.docu_orgi_orga_dk_responsavel = pacote.id_orgao
WHERE docto.docu_dk = :docu_dk
