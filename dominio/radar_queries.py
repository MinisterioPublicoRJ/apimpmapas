query = """
    WITH MAX_DADOS_PACOTE AS (
        select  p.orgi_nm_orgao as nm_max_arq, p.max_value as pct_max_arq,
        p1.orgi_nm_orgao as nm_max_indef, p1.max_value as pct_max_ind,
        p2.orgi_nm_orgao as nm_max_inst, p2.max_value as pct_max_inst,
        p3.orgi_nm_orgao as nm_max_tac, p3.max_value as pct_max_tac,
        p4.orgi_nm_orgao as nm_max_acoes, p4.max_value as pct_max_acoes,
        p.cod_pct
        from (
            select *
            from (
                select  a.orgi_nm_orgao,
                        row_number() over (partition by a.cod_pct order by
                            nr_arquivamentos desc) as num_row,
                        max(nr_arquivamentos) over (partition by a.cod_pct)
                            as max_value,
                        a.cod_pct
                from {schema}.tb_radar_performance p
                join {schema}.atualizacao_pj_pacote a
                on p.orgao_id = a.id_orgao
            ) p
            where p.num_row = 1
        ) p
        join (
            select *
            from (
                select  a.orgi_nm_orgao,
                        row_number() over (partition by a.cod_pct order by
                            nr_indeferimentos desc) as num_row,
                        max(nr_indeferimentos) over (partition by a.cod_pct)
                            as max_value,
                        a.cod_pct
                from {schema}.tb_radar_performance p
                join {schema}.atualizacao_pj_pacote a
                on p.orgao_id = a.id_orgao
            ) p
            where p.num_row = 1

        ) p1 on p.cod_pct = p1.cod_pct
        join (
            select *
            from (
                select  a.orgi_nm_orgao,
                        row_number() over (partition by a.cod_pct order by
                            nr_instauracao desc) as num_row,
                        max(nr_instauracao) over (partition by a.cod_pct)
                            as max_value,
                        a.cod_pct
                from {schema}.tb_radar_performance p
                join {schema}.atualizacao_pj_pacote a
                on p.orgao_id = a.id_orgao
            ) p
            where p.num_row = 1

        ) p2 on p.cod_pct = p2.cod_pct
        join (
            select *
            from (
                select  a.orgi_nm_orgao,
                        row_number() over (partition by a.cod_pct order by
                            nr_tac desc) as num_row,
                        max(nr_tac) over (partition by a.cod_pct) as max_value,
                        a.cod_pct
                from {schema}.tb_radar_performance p
                join {schema}.atualizacao_pj_pacote a
                on p.orgao_id = a.id_orgao
            ) p
            where p.num_row = 1

        ) p3 on p.cod_pct = p3.cod_pct
        join (
            select *
            from (
                select  a.orgi_nm_orgao,
                        row_number() over (partition by a.cod_pct order
                            by nr_acoes desc) as num_row,
                        max(nr_acoes) over (partition by a.cod_pct)
                            as max_value,
                        a.cod_pct
                from {schema}.tb_radar_performance p
                join {schema}.atualizacao_pj_pacote a
                on p.orgao_id = a.id_orgao
            ) p
            where p.num_row = 1

        ) p4 on p.cod_pct = p4.cod_pct
        where p.cod_pct IN (SELECT cod_pct
            FROM {schema}.atualizacao_pj_pacote WHERE
            id_orgao = :orgao_id)
    ),
    MED_ARQUIV_PACOTE AS (
        SELECT cod_pct, appx_median(DISTINCT nr_arquivamentos)
            as med_arquiv
        FROM {schema}.tb_radar_performance
        INNER JOIN {schema}.atualizacao_pj_pacote
        ON id_orgao = orgao_id
        WHERE cod_pct IN (SELECT cod_pct
                          FROM {schema}.atualizacao_pj_pacote
                          WHERE id_orgao = :orgao_id)
        GROUP BY cod_pct
    ),
    MED_TAC_PACOTE AS (
        SELECT cod_pct, appx_median(DISTINCT nr_tac) as med_tac
            FROM {schema}.tb_radar_performance
        INNER JOIN {schema}.atualizacao_pj_pacote
        ON id_orgao = orgao_id
        WHERE cod_pct IN (SELECT cod_pct
                          FROM {schema}.atualizacao_pj_pacote
                          WHERE id_orgao = :orgao_id)
        GROUP BY cod_pct
    ),
    MED_ACOES_PACOTE AS (
        SELECT cod_pct, appx_median(DISTINCT nr_acoes)
            as med_acoes FROM {schema}.tb_radar_performance
        INNER JOIN {schema}.atualizacao_pj_pacote
        ON id_orgao = orgao_id
        WHERE cod_pct IN (SELECT cod_pct
                          FROM {schema}.atualizacao_pj_pacote
                          WHERE id_orgao = :orgao_id)
        GROUP BY cod_pct
    ),
    MED_INSTAU_PACOTE AS (
        SELECT cod_pct, appx_median(DISTINCT nr_instauracao)
            as med_instau FROM {schema}.tb_radar_performance
        INNER JOIN {schema}.atualizacao_pj_pacote
        ON id_orgao = orgao_id
        WHERE cod_pct IN (SELECT cod_pct
                          FROM {schema}.atualizacao_pj_pacote
                          WHERE id_orgao = :orgao_id)
        GROUP BY cod_pct
    ),
    MED_INDEF_PACOTE AS (
        SELECT cod_pct, appx_median(DISTINCT nr_indeferimentos)
            as med_indef FROM {schema}.tb_radar_performance
        INNER JOIN {schema}.atualizacao_pj_pacote
        ON id_orgao = orgao_id
        WHERE cod_pct IN (SELECT cod_pct
                          FROM {schema}.atualizacao_pj_pacote
                          WHERE id_orgao = :orgao_id)
        GROUP BY cod_pct
    ),
    DADOS_ORGAO AS (SELECT * FROM {schema}.tb_radar_performance
    INNER JOIN {schema}.atualizacao_pj_pacote
    ON id_orgao = orgao_id
    WHERE orgao_id = :orgao_id
    )
    SELECT
        DADOS_ORGAO.pacote_atribuicao,
        DADOS_ORGAO.orgao_id,
        DADOS_ORGAO.nr_arquivamentos,
        DADOS_ORGAO.nr_indeferimentos,
        DADOS_ORGAO.nr_instauracao,
        DADOS_ORGAO.nr_tac,
        DADOS_ORGAO.nr_acoes,
        DADOS_ORGAO.dt_calculo,
        MAX_DADOS_PACOTE.*,
        MED_ARQUIV_PACOTE.med_arquiv,
        MED_TAC_PACOTE.med_tac,
        MED_INDEF_PACOTE.med_indef,
        MED_INSTAU_PACOTE.med_instau,
        MED_ACOES_PACOTE.med_acoes,
        DADOS_ORGAO.nr_arquivamentos
            / MAX_DADOS_PACOTE.pct_max_arq * 100 as perc_arquivamentos,
        DADOS_ORGAO.nr_tac
            / MAX_DADOS_PACOTE.pct_max_tac * 100 as perc_tac,
        DADOS_ORGAO.nr_indeferimentos
            / MAX_DADOS_PACOTE.pct_max_ind * 100 as perc_indef,
        DADOS_ORGAO.nr_instauracao
            / MAX_DADOS_PACOTE.pct_max_inst * 100 as perc_instauracao,
        DADOS_ORGAO.nr_acoes
            / MAX_DADOS_PACOTE.pct_max_acoes * 100 as perc_acoes,
        CASE
            WHEN DADOS_ORGAO.nr_arquivamentos <> 0
                AND MED_ARQUIV_PACOTE.med_arquiv <> 0
            THEN
                (DADOS_ORGAO.nr_arquivamentos -
                    MED_ARQUIV_PACOTE.med_arquiv)
                / MED_ARQUIV_PACOTE.med_arquiv
            ELSE 0
        END AS var_med_arquiv,
        CASE
            WHEN DADOS_ORGAO.nr_tac <> 0
                AND MED_TAC_PACOTE.med_tac <> 0
            THEN (DADOS_ORGAO.nr_tac - MED_TAC_PACOTE.med_tac)
                / MED_TAC_PACOTE.med_tac
            ELSE 0
        END AS var_med_tac,
        CASE
            WHEN DADOS_ORGAO.nr_indeferimentos <> 0
                AND MED_INDEF_PACOTE.med_indef <> 0
            THEN (DADOS_ORGAO.nr_indeferimentos -
                    MED_INDEF_PACOTE.med_indef)
                  / MED_INDEF_PACOTE.med_indef
            ELSE 0
        END AS var_med_indef,
        CASE
            WHEN DADOS_ORGAO.nr_instauracao <> 0
                AND MED_INSTAU_PACOTE.med_instau <> 0
            THEN (DADOS_ORGAO.nr_instauracao -
                   MED_INSTAU_PACOTE.med_instau)
                  / MED_INSTAU_PACOTE.med_instau
            ELSE 0
        END AS var_med_instau,
        CASE
            WHEN DADOS_ORGAO.nr_acoes <> 0
                AND MED_ACOES_PACOTE.med_acoes <> 0
            THEN (DADOS_ORGAO.nr_acoes - MED_ACOES_PACOTE.med_acoes)
                / MED_ACOES_PACOTE.med_acoes
            ELSE 0
        END  AS var_med_acoes
        FROM MAX_DADOS_PACOTE
    INNER JOIN DADOS_ORGAO
    ON DADOS_ORGAO.cod_pct = MAX_DADOS_PACOTE.cod_pct
    INNER JOIN MED_ARQUIV_PACOTE
    ON DADOS_ORGAO.cod_pct = MED_ARQUIV_PACOTE.cod_pct
    INNER JOIN MED_TAC_PACOTE
    ON DADOS_ORGAO.cod_pct = MED_TAC_PACOTE.cod_pct
    INNER JOIN MED_ACOES_PACOTE
    ON DADOS_ORGAO.cod_pct = MED_ACOES_PACOTE.cod_pct
    INNER JOIN MED_INDEF_PACOTE
    ON DADOS_ORGAO.cod_pct = MED_INDEF_PACOTE.cod_pct
    INNER JOIN MED_INSTAU_PACOTE
    ON DADOS_ORGAO.cod_pct = MED_INSTAU_PACOTE.cod_pct
"""

field_names = [
    "pacote_atribuicao",
    "orgao_id",
    "nr_arquivamentos",
    "nr_indeferimentos",
    "nr_instauracoes",
    "nr_tac",
    "nr_acoes",
    "dt_calculo",
    "nm_max_arquivamentos",
    "max_pacote_arquivamentos",
    "nm_max_indeferimentos",
    "max_pacote_indeferimentos",
    "nm_max_instauracoes",
    "max_pacote_instauracoes",
    "nm_max_tac",
    "max_pacote_tac",
    "nm_max_acoes",
    "max_pacote_acoes",
    "codigo_pacote",
    "med_pacote_aquivamentos",
    "med_pacote_tac",
    "med_pacote_indeferimentos",
    "med_pacote_instauracoes",
    "med_pacote_acoes",
    "perc_arquivamentos",
    "perc_tac",
    "perc_indeferimentos",
    "perc_instauracoes",
    "perc_acoes",
    "var_med_arquivamentos",
    "var_med_tac",
    "var_med_indeferimentos",
    "var_med_instauracoes",
    "var_med_acoes",
]
