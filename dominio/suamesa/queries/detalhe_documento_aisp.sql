SELECT 
    acervo_inicio,
    acervo_fim,
    CASE acervo_inicio WHEN 0 THEN NULL ELSE (acervo_fim - acervo_inicio)/acervo_inicio END as variacao_acervo,
    aisp_nomes
FROM (
    SELECT 
        SUM(acervo_inicio) as acervo_inicio,
        SUM(acervo_fim) as acervo_fim
    FROM {schema}.tb_detalhe_documentos_orgao
    JOIN (
        SELECT DISTINCT a2.pip_codigo
        FROM {schema}.tb_pip_aisp a1
        JOIN {schema}.tb_pip_aisp a2 ON a1.aisp_codigo = a2.aisp_codigo
        WHERE a1.pip_codigo = :orgao_id
        ) t ON pip_codigo = vist_orgi_orga_dk
    WHERE tipo_detalhe IN ('pip_inqueritos', 'pip_pics')
    AND intervalo = :intervalo
    ) t
JOIN (
    SELECT a.pip_codigo, group_concat(a.aisp_nome) as aisp_nomes
    FROM {schema}.tb_pip_aisp a
    WHERE pip_codigo = :orgao_id
    GROUP BY a.pip_codigo
    ) t2