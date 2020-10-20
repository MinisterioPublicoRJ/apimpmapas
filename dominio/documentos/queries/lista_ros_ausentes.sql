SELECT
    CAST(SUBSTRING(proc_numero, 5, 5) AS INTEGER) num_serial
FROM {schema_opengeo}.seg_pub_in_pol_procedimento
WHERE year(proc_data) = year(now())
    AND CAST(SUBSTRING(proc_numero, 1, 3) AS INTEGER) = :num_delegacia
ORDER BY proc_numero
