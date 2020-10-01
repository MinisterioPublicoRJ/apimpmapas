SELECT 
    cdmatricula as matricula_promotor,
    NMFUNCIONARIO as nome_promotor
FROM RH_FUNCIONARIO
WHERE CPF = :cpf
