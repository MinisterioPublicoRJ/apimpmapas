SELECT id_orgao,
media_orgao,
minimo_orgao,
maximo_orgao,
mediana_orgao,
media_pacote,
minimo_pacote,
maximo_pacote,
mediana_pacote,
media_pacote_t1,
minimo_pacote_t1,
maximo_pacote_t1,
mediana_pacote_t1,
media_orgao_t1,
minimo_orgao_t1,
maximo_orgao_t1,
mediana_orgao_t1,
media_pacote_t2,
minimo_pacote_t2,
maximo_pacote_t2,
mediana_pacote_t2,
media_orgao_t2,
minimo_orgao_t2,
maximo_orgao_t2,
mediana_orgao_t2
FROM {schema}.tb_tempo_tramitacao
WHERE id_orgao = :orgao_id