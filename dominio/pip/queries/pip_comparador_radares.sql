SELECT
    tb_radar.orgao_id,
    tb_pacote.orgao_codamp,
    tb_pacote.orgi_nm_orgao,
    tb_radar.perc_denuncias,
    tb_radar.perc_cautelares,
    tb_radar.perc_acordos,
    tb_radar.perc_arquivamentos,
    tb_radar.perc_aberturas_vista
FROM {schema}.atualizacao_pj_pacote tb_pacote
INNER JOIN {schema}.tb_pip_radar_performance tb_radar
    ON tb_radar.orgao_id = tb_pacote.id_orgao
WHERE tb_pacote.cod_pct in (SELECT cod_pct FROM {schema}.atualizacao_pj_pacote where id_orgao = :orgao_id)
AND tb_radar.orgao_id <> :orgao_id AND tb_pacote.cod_pct >= 200 -- Apenas para diferencia PIP de Tutela
