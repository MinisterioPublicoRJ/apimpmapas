SELECT cdmatricula as matricula,
    CPF as cpf,
    NMFUNCIONARIO as nome,
    SEXO as sexo,
    PESF_PESS_DK as pess_dk
	FROM RH_FUNCIONARIO
    WHERE E_MAIL1 = LOWER(TRIM(:login))
