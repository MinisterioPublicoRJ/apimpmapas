SELECT
    orgi_dk as cdorgao,
    orgi_nm_orgao as nm_org,
    cdmatricula as matricula,
    cpf,
    nmfuncionario as nome,
    SEXO as sexo,
    PESF_PESS_DK as pess_dk
FROM rh_funcionario
JOIN orgi_orgao ON cast(cdorgao as int) = orgi_dk
WHERE cdtipfunc = '1' -- Promotores
AND cdsituacaofunc = '1' -- Situação Normal
AND REGEXP_LIKE(orgi_nm_orgao, '.*PROMOTORIA.*(TUTELA COLETIVA|INVESTIGAÇÃO PENAL).*')
ORDER BY nm_org
