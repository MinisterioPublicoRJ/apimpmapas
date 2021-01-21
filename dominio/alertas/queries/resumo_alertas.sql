SELECT
    alrt.alrt_sigla,
    count(alrt.alrt_sigla) as "count"
FROM {schema}.mmps_alertas alrt
LEFT JOIN (
    SELECT * FROM {schema}.alerta_desabilitado WHERE resolvido = false
) desabilitar ON alrt_sigla = sigla AND orgao_id = :id_orgao
WHERE alrt.dt_partition = :dt_partition
    AND alrt.alrt_orgi_orga_dk = :id_orgao
    AND desabilitar.sigla IS NULL
GROUP BY
    alrt.alrt_sigla
UNION ALL
SELECT 'COMP',
    COUNT(1)
FROM {schema}.atualizacao_pj_pacote
LEFT JOIN (
    SELECT * FROM {schema}.alerta_desabilitado WHERE resolvido = false
) desabilitar ON 'COMP' = sigla AND orgao_id = :id_orgao
INNER JOIN {schema_alertas_compras}.compras_fora_padrao_capital ON
    var_perc >= 20
WHERE UPPER(pacote_atribuicao) LIKE '%%CIDADANIA%%'
    AND orgao_codamp LIKE '%%CAPITAL%%'
    AND id_orgao = :id_orgao
    AND desabilitar.sigla IS NULL
HAVING COUNT(1) > 0