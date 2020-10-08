SELECT
    docu_nr_mp as num_procedimento
FROM
    {schema}.mcpr_documento
WHERE docu_dk = :docu_dk
    AND docu_cldc_dk = 392 -- Apenas IC
