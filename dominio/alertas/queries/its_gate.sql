SELECT gate.itcn_dk as itcn_dk
FROM {schema}.gate_info_tecnica gate
WHERE gate.itcn_docu_dk = :docu_dk