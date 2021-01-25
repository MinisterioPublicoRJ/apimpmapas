WITH RESPONSAVEL_ORGAO AS (
SELECT
    func.NMFUNCIONARIO AS nome,
    func.CDMATRICULA AS matricula,
    func.SEXO AS sexo,
    CASE WHEN CDCARGO IN (74, 75)
        THEN 1
        ELSE 0
    END AS EH_PROMOTOR
FROM RH.FUNCIONARIO func
WHERE CPF = :cpf
)
SELECT
    CASE WHEN ro.EH_PROMOTOR = 1
        THEN ro.matricula
        ELSE f.CDMATRICULA
    END AS matricula,
    CASE WHEN ro.EH_PROMOTOR = 1
        THEN ro.nome
        ELSE f.NMFUNCIONARIO
    END AS nome,
    CASE WHEN ro.EH_PROMOTOR = 1
        THEN ro.sexo
        ELSE f.SEXO
    END AS sexo
FROM RESPONSAVEL_ORGAO ro
LEFT JOIN RH.FUNCIONARIO f ON CDORGAO = :orgao_id
