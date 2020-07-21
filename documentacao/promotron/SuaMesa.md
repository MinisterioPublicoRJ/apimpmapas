# Sua Mesa

*Foto do Sua Mesa Aqui*

O Sua Mesa é o segundo componente do Promotron. Nele podemos ver o número de vistas abertas, procedimentos ativos, e procedimentos finalizados nos últimos 30 dias.

Ele está separado em duas partes:

* Sua Mesa Caixinhas: Correspondem aos quadrados na parte superior.
* Sua Mesa Detalhes: Correspondem aos detalhes que aparecem na parte inferior ao clicar em determinadas Caixinhas.

## Sua Mesa Caixinhas

### User Manual

As Caixinhas correspondem sempre a um número calculado de acordo com determinada regra de negócio. O cálculo é feito diretamente no Oracle, de forma que os dados utilizados são os disponíveis em tempo real (embora possa haver cacheamento). Há, no momento, 8 tipos de regras definidas (formando, assim 8 tipos de Caixinhas diferentes). São estas:

- Vistas Abertas (Tutela e PIP): Vistas abertas para um determinado órgão e CPF.
- Investigações (Tutela): Número de investigações em curso de uma Tutela Coletiva.
- Processos (Tutela): Número de processos em juízo de uma Tutela Coletiva.
- Finalizados (Tutela): Número de documentos finalizados nos últimos 30 dias em uma tutela.
- Inquéritos (PIP): Número de inquéritos ativos em uma PIP.
- PICs (PIP): Número de PICs ativas em uma PIP.
- AISP (PIP): Número de inquéritos + PICs ativos na AISP de uma PIP.
- Finalizados (PIP): Número de documentos finalizados nos últimos 30 dias para PIPs.

As regras para cada uma destas caixinhas são as seguintes:

#### Vistas Abertas

Correspondem às vistas abertas para o órgão e CPF selecionados, e onde a data de fechamento seja maior do que a data atual ou nula.

A query correspondente no BDA seria a seguinte:

```
SELECT COUNT(*)
FROM {schema_exadata}.MCPR_VISTA
JOIN {schema_exadata}.MCPR_PESSOA_FISICA
  ON vist_pesf_pess_dk_resp_andam = pesf_pess_dk
WHERE vist_orgi_orga_dk = {ORGAO_DADO}
AND pesf_cpf = {CPF_DADO}
AND (vist_dt_fechamento_vista IS NULL 
  OR vist_dt_fechamento_vista > current_timestamp())
```

Essa Caixinha serve para qualquer tipo de órgão, sendo usada tanto para Tutelas quanto PIPs.

#### Investigações (Tutela)

Esta Caixinha é para uso apenas de Tutela Coletiva. Ela busca os documentos em andamento, e que não foram cancelados, das seguintes classes:

| cldc_dk | hierarquia |
| :- | :- |
| 395 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Preparatório |
| 392 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Inquérito Civil |
| 51223 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Administrativo > Procedimento Administrativo de tutela de interesses individuais indisponíveis |
| 51222 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Administrativo > Procedimento Administrativo de outras atividades não sujeitas a inquérito civil |
| 51220 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Administrativo > Procedimento Administrativo de acompanhamento de Políticas Públicas |
| 51221 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Administrativo > Procedimento Administrativo de acompanhamento de TAC |
| 51219 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Administrativo > Procedimento Administrativo de acompanhamento de Instituições |

#### Processos (Tutela)

Esta Caixinha é para uso apenas de Tutela Coletiva. Ela busca os documentos em andamento, e que não foram cancelados, das seguintes classes:

| cldc_dk | hierarquia |
| :- | :- |
| 323 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  > Processo de Execução Trabalhista  > Execução Provisória em Autos Suplementares |
| 319 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  > Processo de Execução Trabalhista  > Execução de Título Extrajudicial |
| 320 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  > Processo de Execução Trabalhista  > Execução de Termo de Ajuste de Conduta |
| 18 | SUPREMO TRIBUNAL FEDERAL  > Ação Rescisória |
| 126 | SUPERIOR TRIBUNAL DE JUSTIÇA > Ação Rescisória |
| 127 | SUPERIOR TRIBUNAL DE JUSTIÇA > Ação de Improbidade Administrativa |
| 159 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Conhecimento  > Procedimento de Conhecimento  > Procedimentos Especiais  > Procedimentos Especiais de Jurisdição Contenciosa  > Ação Rescisória |
| 175 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Conhecimento  > Procedimento de Conhecimento  > Procedimentos Especiais  > Procedimentos Regidos por Outros Códigos, Leis Esparsas e Regimentos  > Ação Civil Coletiva |
| 176 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Conhecimento  > Procedimento de Conhecimento  > Procedimentos Especiais  > Procedimentos Regidos por Outros Códigos, Leis Esparsas e Regimentos  > Ação Civil de Improbidade Administrativa |
| 177 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Conhecimento  > Procedimento de Conhecimento  > Procedimentos Especiais  > Procedimentos Regidos por Outros Códigos, Leis Esparsas e Regimentos  > Ação Civil Pública |
| 582 | PROCESSO CRIMINAL  > Execução Criminal  > Execução Provisória |
| 441 | JUIZADOS DA INFÂNCIA E DA JUVENTUDE  > Seção Cível  >  Processo de Conhecimento  >  Ação Civil Pública |
| 51205 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  >  Execução de Título Extrajudicial  > Execução de Título Extrajudicial contra a Fazenda Pública |
| 51217 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  >  Execução de Título Extrajudicial  > Execução de Título Extrajudicial |
| 51218 | PROCESSO CÍVEL E DO TRABALHO  > Processo de Execução  >  Execução de Título Extrajudicial  > Execução Extrajudicial de Alimentos |

Além disso, a regra desta caixinha inclui uma etapa adicional em que o número externo do documento (`docu_nr_externo`) é utilizado para extrair o ano do documento, e o código do TJ.

Caso o ano extraído do número externo bata com o ano do documento registrado no banco, e o número externo do TJ seja encontrado na posição correta, ele é contabilizado.

#### Finalizados (Tutela)

Esta Caixinha é para uso apenas de Tutelas.

Ela busca os documentos que tiveram pelo menos um andamento finalizador, dentro de regras de andamento definidas. Os andamentos (e o documento correspondente) não podem ter sido cancelados.

Além disso, essa contagem é feita apenas para andamentos que ocorreram nos últimos 30 dias.

Desarquivamentos *não* são levados em consideração no cálculo. Isso quer dizer que, caso um documento seja arquivado e posteriormente desarquivado neste período de 30 dias, ele contará como finalizado neste componente.

As regras de negócio definidas para os Finalizados de Tutela são as seguintes:

| tppr_dk | hierarquia |
| :- | :- |
| 6015 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) |
| 6016 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) |
| 6017 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Extinção da Punibilidade por Outros Fundamentos |
| 6018 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório) |
| 6019 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Em razão de o adolescente ter alcançado a maioridade penal |
| 6020 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Extinção da Punibilidade por Outros Fundamentos |
| 6021 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório) |
| 6022 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Em razão de o adolescente ter alcançado a maioridade penal |
| 6251 | MEMBRO > Ajuizamento de Ação > Petição Inicial |
| 6324 | MEMBRO > Arquivamento |
| 6325 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior |
| 6326 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral com TAC |
| 6327 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) |
| 6328 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) |
| 6329 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário |
| 6330 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial |
| 6331 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Desconhecimento do Autor |
| 6332 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Inexistência de Crime |
| 6333 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Prescrição |
| 6334 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Decadência |
| 6335 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Retratação Lei Maria da Penha |
| 6336 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Pagamento de Débito Tributário |
| 6337 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral |
| 6338 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Desconhecimento do Autor |
| 6339 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Inexistência de Crime |
| 6340 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Prescrição |
| 6341 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Decadência |
| 6342 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Retratação Lei Maria da Penha |
| 6343 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Pagamento de Débito Tributário |
| 6344 | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara |
| 6345 | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Parcial |
| 6346 | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Integral |
| 6350 | MEMBRO > Homologação de Arquivamento |
| 6548 | MEMBRO > Termo de reconhecimento de paternidade |
| 6553 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Insuficiência de Provas |
| 6591 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Falta de condições para o regular exercício do direito de ação |
| 6593 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Falta de condições para o exercício do direito de ação |
| 6644 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Resolução da questão |
| 6645 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Não configuração de ilícito |
| 6655 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Com TAC |
| 6656 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC |
| 6657 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Resolução da questão |
| 6658 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Não configuração de ilícito |
| 6659 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Inveracidade do fato |
| 6660 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Prescrição |
| 6661 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Perda do objeto sem resolução da questão |
| 6662 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Falta de uma das condições da ação |
| 6663 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Outros |
| 6664 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Resolução da questão |
| 6665 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Não configuração de ilícito |
| 6666 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Inveracidade do fato |
| 6667 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Perda do objeto sem resolução da questão |
| 6668 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Falta de uma das condições da ação |
| 6669 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Outros |
| 6670 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Com TAC |
| 6671 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC |
| 6672 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Resolução da questão |
| 6673 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Não configuração de ilícito |
| 6674 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Inveracidade do fato |
| 6675 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Perda do objeto sem resolução da questão |
| 6676 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Falta de uma das condições da ação |
| 6677 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Outros |
| 6678 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Inveracidade do fato |
| 6679 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Prescrição |
| 6680 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Perda do objeto sem resolução da questão |
| 6681 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Falta de uma das condições da ação |
| 6682 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Outros |
| 7737 | SERVIDOR > Atualização da fase para "Finalizado" em decorrência da vinculação como juntada |
| 7745 | MEMBRO > Arquivamento > De notícia de fato ou procedimento de atribuição originária do PGJ |
| 7834 | MEMBRO > Indeferimento de pedido de desarquivamento |
| 7869 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos |
| 7870 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos |
| 7871 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Morte do Agente |
| 7872 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Morte de Agente |
| 7912 | MEMBRO > Arquivamento > Com Remessa ao PRE/PGE |

#### Inquéritos (PIP)

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em andamento, e que não foram cancelados, das seguintes classes:

| cldc_dk | hierarquia |
| :- | :- |
| 3 | PROCESSO MILITAR  > PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Inquérito Policial Militar |
| 494 | PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Inquérito Policial |

#### PICs (PIP)

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em andamento, e que não foram cancelados, das seguintes classes:

| cldc_dk | hierarquia |
| :- | :- |
| 590 | PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Procedimento Investigatório Criminal (PIC-MP) |

#### AISPs (PIP)

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em andamento, e que não foram cancelados, para todas as promotorias pertencentes à AISP da promotoria sendo analisada, das seguintes classes:

| cldc_dk | hierarquia |
| :- | :- |
| 3 | PROCESSO MILITAR  > PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Inquérito Policial Militar |
| 494 | PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Inquérito Policial |
| 590 | PROCESSO CRIMINAL  > Procedimentos Investigatórios  > Procedimento Investigatório Criminal (PIC-MP) |

#### Finalizados (PIP)

Esta Caixinha é para uso apenas de PIPs.

Da mesma forma que a da Tutela, ela busca os documentos que tiveram pelo menos um andamento finalizador, dentro de regras de andamento definidas. Os andamentos (e o documento correspondente) não podem ter sido cancelados.

Além disso, a contagem é feita apenas para andamentos que ocorreram nos últimos 30 dias.

Desarquivamentos *não* são levados em consideração no cálculo. Isso quer dizer que, caso um documento seja arquivado e posteriormente desarquivado neste período de 30 dias, ele contará como finalizado neste componente.

As regras de negócio definidas para os Finalizados de PIP são as seguintes:

| tppr_dk | hierarquia |
| :- | :- |
| 6017 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Extinção da Punibilidade por Outros Fundamentos |
| 6018 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório) |
| 6019 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Em razão de o adolescente ter alcançado a maioridade penal |
| 6253 | MEMBRO > Ajuizamento de Ação > Denúncia > Escrita |
| 6272 | MEMBRO > Aditamento > Denúncia |
| 6338 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Desconhecimento do Autor |
| 6339 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Inexistência de Crime |
| 6340 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Prescrição |
| 6341 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Decadência |
| 6342 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Retratação Lei Maria da Penha |
| 6343 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Pagamento de Débito Tributário |
| 6346 | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Integral |
| 6350 | MEMBRO > Homologação de Arquivamento |
| 6359 | MEMBRO > Decisão Artigo 28 CPP / 397 CPPM > Confirmação Integral > Arquivamento |
| 6361 | MEMBRO > Proposta de transação penal |
| 6362 | MEMBRO > Proposta de suspensão condicional do processo |
| 6377 | MEMBRO > Ciência > Sentença > Extintiva pela prescrição |
| 6378 | MEMBRO > Ciência > Sentença > Extintiva por outras causas |
| 6392 | MEMBRO > Ciência > Arquivamento |
| 6436 | MEMBRO > Ratificação de Denúncia |
| 6524 | SERVIDOR > Arquivamento |
| 6591 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Falta de condições para o regular exercício do direito de ação |
| 6625 | SERVIDOR > Informação sobre ajuizamento do documento no Poder Judiciário |
| 6669 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Outros |
| 6682 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Outros |
| 6718 | SERVIDOR > Informação sobre o encaminhamento a Juízo para juntada a processo judicial |
| 7737 | SERVIDOR > Atualização da fase para "Finalizado" em decorrência da vinculação como juntada |
| 7745 | MEMBRO > Arquivamento > De notícia de fato ou procedimento de atribuição originária do PGJ |
| 7811 | SERVIDOR > Finalização de processo judicial |
| 7834 | MEMBRO > Indeferimento de pedido de desarquivamento |
| 7871 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Morte do Agente |
| 7915 | MEMBRO > Acordo de Não Persecução Penal > Oferecimento de acordo |

### Estrutura do Código

Falar sobre a estrutura de DAO Factory
Regras definidas dentro das funções no backend
Pega dados diretamente do Oracle pela ORM do DJango
Falar sobre uso das queries no managers.py também

### Dependências

Não há dependências de tabelas (a não ser as do Oracle).

### Troubleshooting

## Sua Mesa Detalhe

### User Manual

### Estrutura do Código

### Dependências

### Troubleshooting
