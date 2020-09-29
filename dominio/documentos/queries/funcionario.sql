SELECT
    func.cdmatricula as matricula,
    func.nmfuncionario as nome,
    carg.nmcargo as cargo
FROM exadata_dev.rh_funcionario func
JOIN exadata_dev.rh_cargos carg ON carg.cdcargo = func.cdcargo
WHERE cdmatricula = :matricula;