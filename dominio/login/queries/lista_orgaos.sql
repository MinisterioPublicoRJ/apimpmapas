select
	h.cdorgao as cdorgao,
	o.ORGI_NM_ORGAO as nm_org
from hist_func h
	join MPRJ_VW_FUNCIONARIO f on f.cdmatricula = h.cdmatricula
	join RH_FUNCIONARIO rhf on rhf.CDMATRICULA = h.cdmatricula
	join ORGI_ORGAO o on o.ORGI_CDORGAO = h.cdorgao
	left join ORGI_GRUPO_PREF grp ON o.ORGI_GRPF_DK = grp.GRPF_DK
where rhf.E_MAIL1 = LOWER(TRIM(:login))                           -- Matrícula igual à procurada
	  and (dtfimexerreal is null or dtfimexerreal > sysdate)      -- Data de saída no futuro ou não informada
	  and (o.ORGI_DT_FIM is null or o.ORGI_DT_FIM > sysdate)      -- Data de extinção do órgão no futuro ou não informada
	  and ((f.CDTIPFUNC = 1                                       -- Que seja MP_ATIVO
			and h.CDMOTIVOINI not in ('AS')                       -- Cujo motivo de início não seja AS
			and (h.obs is null or (                               -- E que caso tenha observações, elas não contenham
				lower(h.obs) not like '%exclusivamente%'          -- as palavras 'exclusivamente' e 'especificamente'
				and lower(h.obs) not like '%especificamente%'
			))) or (f.CDTIPFUNC <> 1))                            -- Ou que não seja MP_ATIVO

GROUP BY h.cdorgao, o.ORGI_NM_ORGAO
