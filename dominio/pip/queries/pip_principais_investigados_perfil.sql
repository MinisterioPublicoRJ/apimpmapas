SELECT pess_dk, pesf_nm_pessoa_fisica, pesf_nm_mae, pesf_cpf, pesf_nr_rg, pesf_dt_nasc
FROM {schema_exadata}.mcpr_pessoa_fisica
JOIN {schema}.tb_pip_investigados_representantes ON pess_dk = pesf_pess_dk
WHERE representante_dk = :dk
ORDER BY pess_dk