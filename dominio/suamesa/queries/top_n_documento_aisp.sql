SELECT 
    group_concat(aisp_nome) as nm_aisp,
    max(valor) as valor
FROM (
    SELECT 
        aisp_nome,
        SUM({nm_campo}) as valor,
        MAX(pip_codigo) as pmax 
    FROM {schema}.tb_detalhe_documentos_orgao
    JOIN {schema}.tb_pip_aisp ON pip_codigo = vist_orgi_orga_dk
    WHERE tipo_detalhe IN ('pip_inqueritos', 'pip_pics')
    GROUP BY aisp_nome
    ) t
GROUP BY pmax
ORDER BY valor DESC
LIMIT :n