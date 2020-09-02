SELECT pesf_nm_pessoa_fisica, pesf_cpf, pesf_nr_rg, pesf_nm_mae, pesf_dt_nasc
FROM {schema}.mcpr_pessoa_fisica
WHERE pesf_pess_dk = :dk