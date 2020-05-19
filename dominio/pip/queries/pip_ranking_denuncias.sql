SELECT
    assu_nm_assunto,
    COUNT(distinct docu_dk),
    SUM(COUNT(distinct docu_dk)) OVER () as total,
    COUNT(distinct docu_dk) / SUM(COUNT(distinct docu_dk)) OVER () as percentual
FROM {schema}.MCPR_DOCUMENTO
JOIN {schema}.mcpr_vista ON vist_docu_dk = docu_dk
LEFT JOIN {schema}.mcpr_assunto_documento ON asdo_docu_dk = docu_dk
LEFT JOIN {schema}.mcpr_assunto ON asdo_assu_dk = assu_dk
WHERE vist_orgi_orga_dk = :orgao_id --Somente documentos que tiveram vista na PIP
AND docu_cldc_dk IN (3, 494, 590) --Somente documentos das classes IC, PP, PA
GROUP BY assu_nm_assunto
ORDER BY 2 DESC
LIMIT 3
