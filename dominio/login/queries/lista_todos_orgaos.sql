SELECT
    orgi_dk as cdorgao,
    orgi_nm_orgao as nm_org,
    cdmatricula as matricula,
    cpf,
    nmfuncionario as nome,
    SEXO as sexo,
    PESF_PESS_DK as pess_dk,
    'PJ' AS cargo
FROM rh_funcionario rhf
INNER JOIN orgi_orgao ON cast(cdorgao as int) = orgi_dk
LEFT JOIN RH_CARGOS cgo ON rhf.cdcargo = cgo.cdcargo
WHERE cdtipfunc != '2' --Exclui MP Inativo
AND cdsituacaofunc = '1' -- Situação Normal
AND REGEXP_LIKE(orgi_nm_orgao, '.*PROMOTORIA.*(TUTELA COLETIVA|INVESTIGAÇÃO PENAL).*')
AND cgo.NMCARGO = 'PROMOTOR DE JUSTICA'
ORDER BY nm_org
