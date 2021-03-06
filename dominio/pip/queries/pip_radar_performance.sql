SELECT aisp_codigo,
aisp_nome,
orgao_id,
nr_denuncias,
nr_cautelares,
nr_acordos_n_persecucao,
nr_arquivamentos,
nr_aberturas_vista,
max_denuncias,
max_cautelares,
max_acordos,
max_arquivamentos,
max_vistas,
perc_denuncias,
perc_cautelares,
perc_acordos,
perc_arquivamentos,
perc_aberturas_vista,
med_denuncias,
med_cautelares,
med_acordos,
med_arquivamentos,
med_vistas,
var_med_denuncias,
var_med_cautelares,
var_med_acordos,
var_med_arquivamentos,
var_med_aberturas_vista,
dt_calculo,
nm_max_denuncias,
nm_max_cautelares,
nm_max_acordos,
nm_max_arquivamentos,
nm_max_aberturas,
cod_pct
FROM {schema}.tb_pip_radar_performance
WHERE orgao_id = :orgao_id
