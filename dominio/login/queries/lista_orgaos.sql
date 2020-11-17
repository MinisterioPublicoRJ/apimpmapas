SELECT
	hist.cdorgao as cdorgao,
	orgi.ORGI_NM_ORGAO as nm_org,
    func.cdmatricula as matricula,
    func.cpf,
    func.nmfuncionario as nome,
    func.SEXO as sexo,
    func.PESF_PESS_DK as pess_dk
FROM rh.HIST_FUNC hist
    JOIN rh_funcionario func ON func.cdmatricula = hist.cdmatricula
    JOIN orgi_orgao orgi ON cast(hist.cdorgao as INT) = orgi.orgi_dk
    JOIN rh.tipo_funcionario tf ON tf.cdtipfunc = func.CDTIPFUNC 
WHERE func.E_MAIL1 = LOWER(TRIM(:login))
    AND (hist.dtfimexerreal IS NULL OR hist.dtfimexerreal >= SYSDATE)
    AND orgi.orgi_tpor_dk = 1
    AND func.CDSITUACAOFUNC = '1'
    AND func.CDTIPFUNC = 1 -- APENAS PROMOTOR
	AND tf.sit_func = 'A'
