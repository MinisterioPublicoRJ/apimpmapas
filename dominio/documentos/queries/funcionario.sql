SELECT
    func.cdmatricula as matricula,
    func.nmfuncionario as nome
FROM {schema}.rh_funcionario func
WHERE 
    func.cdmatricula = :matricula
    AND func.cdtipfunc IN (1, 2)
