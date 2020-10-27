-- Usando o codigo das pips diretamente (cacheado no back), e não precisa retornar a lista de nomes
SELECT 
    acervo_inicio,
    acervo_fim,
    CASE WHEN (acervo_fim - acervo_inicio) = 0 THEN 0 ELSE (acervo_fim - acervo_inicio)/acervo_inicio END as variacao_acervo
FROM (
    SELECT 
        SUM(acervo_inicio) as acervo_inicio,
        SUM(acervo_fim) as acervo_fim
    FROM {schema}.tb_detalhe_documentos_orgao
    WHERE tipo_detalhe IN ('pip_inqueritos', 'pip_pics')
    AND intervalo = :intervalo
    AND vist_orgi_orga_dk IN :orgaos_aisp
) t