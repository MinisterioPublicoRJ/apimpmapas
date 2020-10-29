SELECT
    pess_dk,
    pess_pesf_nm_pessoa_fisica,
    pess_pesf_nm_mae,
    pess_pesf_cpf,
    pess_pesf_nr_rg,
    pess_pesf_dt_nasc,
    pess_pesj_nm_pessoa_juridica,
    pess_pesj_cnpj
FROM {schema}.tb_pip_investigados_representantes
WHERE representante_dk = :dk AND rep_last_digit = :digit
ORDER BY pess_dk