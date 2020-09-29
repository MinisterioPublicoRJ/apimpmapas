SELECT pess_nm_pessoa,
representante_dk,
pip_codigo,
nr_investigacoes,
flag_multipromotoria,
flag_top50
FROM {schema}.tb_pip_investigados
WHERE pip_codigo = :orgao_id