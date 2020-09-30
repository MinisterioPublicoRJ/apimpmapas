SELECT
    func.cdmatricula as matricula,
    func.nmfuncionario as nome,
    carg.nmcargo as cargo
FROM {schema}.rh_funcionario func
JOIN {schema}.rh_cargos carg ON carg.cdcargo = func.cdcargo
WHERE func.cdmatricula = :matricula
