SELECT DISTINCT
 CASE
    WHEN org.ORGI_TPOR_DK = 1 THEN org.ORGI_DK
    WHEN prom.ORGI_DK IS NULL THEN org.ORGI_DK
    ELSE prom.ORGI_DK
 END AS cdorgao,
 CASE
   WHEN org.ORGI_TPOR_DK = 1 THEN org.ORGI_NM_ORGAO
   WHEN prom.ORGI_NM_ORGAO IS NULL THEN org.ORGI_NM_ORGAO
   ELSE prom.ORGI_NM_ORGAO
END AS nm_orgao,
func.CDMATRICULA AS matricula,
func.CPF,
func.NMFUNCIONARIO AS nome,
func.SEXO,
func.PFVW_DK,
CASE
    WHEN cgo.NMCARGO = 'PROMOTOR DE JUSTICA' THEN 'PJ'
    WHEN func.ATVD_SIGLA_ATIVIDADE IN ('A5T', 'ASS') THEN 'ASS'
    WHEN func.ATVD_SIGLA_ATIVIDADE = 'SEC' THEN 'SEC'
END AS cargo
FROM RH.RH_VW_FUNCIONARIO func
INNER JOIN RH.HIST_FUNC hist ON hist.CDMATRICULA  = func.CDMATRICULA
INNER JOIN ORGI.ORGI_ORGAO org ON org.ORGI_DK = TO_NUMBER(hist.CDORGAO)
LEFT JOIN ORGI.ORGI_AUXILIA aux ON aux.ORAU_ORGI_DK = TO_NUMBER(hist.CDORGAO)
LEFT JOIN ORGI.ORGI_ORGAO prom ON prom.ORGI_DK = aux.ORAU_ORGI_DK_AUXILIA
LEFT JOIN RH_CARGOS cgo ON func.cdcargo = cgo.cdcargo
WHERE func.E_MAIL1 = LOWER(TRIM(:login))
    AND (hist.DTFIMEXERREAL IS NULL OR hist.DTFIMEXERREAL >= SYSDATE)
    AND func.CDCARGO != 70 -- DDL da VW mosta que 70 é Procurador
    AND func.CDSITUACAOFUNC = 1 -- SELECT * FROM RH.SITUACAO_FUNC sf | Situacao Normal
    AND func.CDTIPFUNC != 2 -- SELECT * FROM RH.TIPO_FUNCIONARIO tf  | MP Inativo
    AND (func.ATVD_SIGLA_ATIVIDADE IN ('A5T', 'ASS', 'SEC') OR cgo.NMCARGO = 'PROMOTOR DE JUSTICA')
