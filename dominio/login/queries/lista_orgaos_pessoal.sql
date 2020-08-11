SELECT
	o.ORGI_CDORGAO AS cdorgao,
	o.ORGI_NM_ORGAO AS nm_org,
    rhf.cdmatricula as matricula,
    rhf.cpf,
    rhf.nmfuncionario as nome,
    rhf.SEXO as sexo,
    rhf.PESF_PESS_DK as pess_dk
FROM
	RH_MOVIMENTACAO_FUNCIONARIO mf
    JOIN RH_FUNCIONARIO rhf ON rhf.CDMATRICULA = mf.MOFU_CDMATRICULA
	JOIN ORGI_ORGAO o ON mf.MOFU_ORGI_DK = o.ORGI_DK
	left join ORGI_GRUPO_PREF grp ON o.ORGI_GRPF_DK = grp.GRPF_DK
WHERE
	rhf.E_MAIL1 = LOWER(TRIM(:login))
	AND (MOFU_DT_FIM is null or MOFU_DT_FIM > sysdate)

GROUP BY o.ORGI_CDORGAO, o.ORGI_NM_ORGAO, rhf.cdmatricula, rhf.cpf, rhf.nmfuncionario, rhf.SEXO, rhf.PESF_PESS_DK
