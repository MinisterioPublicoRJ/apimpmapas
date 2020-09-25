SELECT
    pess_dk,
    pesf_nm_pessoa_fisica,
    pesf_nm_mae,
    pesf_cpf,
    pesf_nr_rg,
    pesf_dt_nasc,
    pesj_nm_pessoa_juridica,
    pesj_cnpj
FROM {schema}.tb_pip_investigados_representantes
LEFT JOIN {schema_exadata}.mcpr_pessoa_fisica ON pess_dk = pesf_pess_dk
LEFT JOIN {schema_exadata}.mcpr_pessoa_juridica ON pess_dk = pesj_pess_dk
WHERE representante_dk = :dk
ORDER BY pess_dk