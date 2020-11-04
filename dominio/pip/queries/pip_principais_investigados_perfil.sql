SELECT
    pess_dk,
    pess_pesf_nm_pessoa_fisica,
    pess_pesf_nm_mae,
    pess_pesf_cpf,
    pess_pesf_nr_rg,
    pess_pesf_dt_nasc,
    pess_pesj_nm_pessoa_juridica,
    pess_pesj_cnpj
FROM {schema}.tb_pip_investigados_representantes R
WHERE representante_dk = :dk AND rep_last_digit = :digit
AND EXISTS (
    SELECT 1
    FROM {schema}.tb_pip_investigados_procedimentos P
    WHERE P.rep_last_digit = :digit
    AND cod_pct IN :pcts
    AND P.pess_dk = R.pess_dk
)
ORDER BY pess_dk