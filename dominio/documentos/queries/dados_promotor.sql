SELECT
    cdmatricula as matricula_promotor,
    NMFUNCIONARIO as nome_promotor,
    sexo
FROM {schema}.RH_FUNCIONARIO
WHERE CPF = :cpf
    AND cdtipfunc = '1'
