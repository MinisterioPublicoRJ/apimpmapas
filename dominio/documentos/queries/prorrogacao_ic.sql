SELECT
    docu_nr_mp as num_procedimento
FROM
    {schema}.mcpr_documento
WHERE docu_dk = :docu_dk
