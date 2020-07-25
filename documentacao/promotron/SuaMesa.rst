Sua Mesa
========

.. figure:: figuras/sua_mesa.png
   :alt: SuaMesaFigura

   SuaMesaFigura

O Sua Mesa é o segundo componente do Promotron. Nele podemos ver o
número de vistas abertas, procedimentos ativos, e procedimentos
finalizados nos últimos 30 dias.

Ele está separado em duas partes:

-  Sua Mesa Caixinhas: Correspondem aos quadrados na parte superior.
-  Sua Mesa Detalhes: Correspondem aos detalhes que aparecem na parte
   inferior ao clicar em determinadas Caixinhas.

Sua Mesa Caixinhas
------------------

.. figure:: figuras/sua_mesa_caixinhas.png
   :alt: SuaMesaCaixinhasFigura

   SuaMesaCaixinhasFigura

User Manual
~~~~~~~~~~~

As Caixinhas correspondem sempre a um número calculado de acordo com
determinada regra de negócio. O cálculo é feito diretamente no Oracle,
de forma que os dados utilizados são os disponíveis em tempo real
(embora possa haver cacheamento). Há, no momento, 8 tipos de regras
definidas (formando, assim 8 tipos de Caixinhas diferentes). São estas:

-  Vistas Abertas (Tutela e PIP): Vistas abertas para um determinado
   órgão e CPF.
-  Investigações (Tutela): Número de investigações em curso de uma
   Tutela Coletiva.
-  Processos (Tutela): Número de processos em juízo de uma Tutela
   Coletiva.
-  Finalizados (Tutela): Número de documentos finalizados nos últimos 30
   dias em uma tutela.
-  Inquéritos (PIP): Número de inquéritos ativos em uma PIP.
-  PICs (PIP): Número de PICs ativas em uma PIP.
-  AISP (PIP): Número de inquéritos + PICs ativos na AISP de uma PIP.
-  Finalizados (PIP): Número de documentos finalizados nos últimos 30
   dias para PIPs.

As regras para cada uma destas caixinhas são as seguintes:

Vistas Abertas
^^^^^^^^^^^^^^

Correspondem às vistas abertas para o órgão e CPF selecionados, e onde a
data de fechamento seja maior do que a data atual ou nula.

A query correspondente no BDA seria a seguinte:

::

   SELECT COUNT(*)
   FROM {schema_exadata}.MCPR_VISTA
   JOIN {schema_exadata}.MCPR_PESSOA_FISICA
     ON vist_pesf_pess_dk_resp_andam = pesf_pess_dk
   WHERE vist_orgi_orga_dk = {ORGAO_DADO}
   AND pesf_cpf = {CPF_DADO}
   AND (vist_dt_fechamento_vista IS NULL 
     OR vist_dt_fechamento_vista > current_timestamp())

Essa Caixinha serve para qualquer tipo de órgão, sendo usada tanto para
Tutelas quanto PIPs.

Investigações (Tutela)
^^^^^^^^^^^^^^^^^^^^^^

Esta Caixinha é para uso apenas de Tutela Coletiva. Ela busca os
documentos em andamento, e que não foram cancelados, das seguintes
classes:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 395                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Preparatório    |
+-----------------------------------+-----------------------------------+
| 392                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Inquérito Civil              |
+-----------------------------------+-----------------------------------+
| 51223                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | tutela de interesses individuais  |
|                                   | indisponíveis                     |
+-----------------------------------+-----------------------------------+
| 51222                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | outras atividades não sujeitas a  |
|                                   | inquérito civil                   |
+-----------------------------------+-----------------------------------+
| 51220                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Políticas       |
|                                   | Públicas                          |
+-----------------------------------+-----------------------------------+
| 51221                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de TAC             |
+-----------------------------------+-----------------------------------+
| 51219                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Instituições    |
+-----------------------------------+-----------------------------------+

Processos (Tutela)
^^^^^^^^^^^^^^^^^^

Esta Caixinha é para uso apenas de Tutela Coletiva. Ela busca os
documentos em andamento, e que não foram cancelados, das seguintes
classes:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 323                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução Provisória em Autos      |
|                                   | Suplementares                     |
+-----------------------------------+-----------------------------------+
| 319                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução de Título Extrajudicial  |
+-----------------------------------+-----------------------------------+
| 320                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Processo   |
|                                   | de Execução Trabalhista >         |
|                                   | Execução de Termo de Ajuste de    |
|                                   | Conduta                           |
+-----------------------------------+-----------------------------------+
| 18                                | SUPREMO TRIBUNAL FEDERAL > Ação   |
|                                   | Rescisória                        |
+-----------------------------------+-----------------------------------+
| 126                               | SUPERIOR TRIBUNAL DE JUSTIÇA >    |
|                                   | Ação Rescisória                   |
+-----------------------------------+-----------------------------------+
| 127                               | SUPERIOR TRIBUNAL DE JUSTIÇA >    |
|                                   | Ação de Improbidade               |
|                                   | Administrativa                    |
+-----------------------------------+-----------------------------------+
| 159                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Especiais de        |
|                                   | Jurisdição Contenciosa > Ação     |
|                                   | Rescisória                        |
+-----------------------------------+-----------------------------------+
| 175                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil Coletiva  |
+-----------------------------------+-----------------------------------+
| 176                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil de        |
|                                   | Improbidade Administrativa        |
+-----------------------------------+-----------------------------------+
| 177                               | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Conhecimento >        |
|                                   | Procedimento de Conhecimento >    |
|                                   | Procedimentos Especiais >         |
|                                   | Procedimentos Regidos por Outros  |
|                                   | Códigos, Leis Esparsas e          |
|                                   | Regimentos > Ação Civil Pública   |
+-----------------------------------+-----------------------------------+
| 582                               | PROCESSO CRIMINAL > Execução      |
|                                   | Criminal > Execução Provisória    |
+-----------------------------------+-----------------------------------+
| 441                               | JUIZADOS DA INFÂNCIA E DA         |
|                                   | JUVENTUDE > Seção Cível >         |
|                                   | Processo de Conhecimento > Ação   |
|                                   | Civil Pública                     |
+-----------------------------------+-----------------------------------+
| 51205                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução de Título Extrajudicial  |
|                                   | contra a Fazenda Pública          |
+-----------------------------------+-----------------------------------+
| 51217                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução de Título Extrajudicial  |
+-----------------------------------+-----------------------------------+
| 51218                             | PROCESSO CÍVEL E DO TRABALHO >    |
|                                   | Processo de Execução > Execução   |
|                                   | de Título Extrajudicial >         |
|                                   | Execução Extrajudicial de         |
|                                   | Alimentos                         |
+-----------------------------------+-----------------------------------+

Além disso, a regra desta caixinha inclui uma etapa adicional em que o
número externo do documento (``docu_nr_externo``) é utilizado para
extrair o ano do documento, e o código do TJ.

Caso o ano extraído do número externo bata com o ano do documento
registrado no banco, e o número externo do TJ seja encontrado na posição
correta, ele é contabilizado.

Finalizados (Tutela)
^^^^^^^^^^^^^^^^^^^^

Esta Caixinha é para uso apenas de Tutelas.

Ela busca os documentos que tiveram pelo menos um andamento finalizador,
dentro de regras de andamento definidas. Os andamentos (e o documento
correspondente) não podem ter sido cancelados.

Além disso, essa contagem é feita apenas para andamentos que ocorreram
nos últimos 30 dias.

Desarquivamentos *não* são levados em consideração no cálculo. Isso quer
dizer que, caso um documento seja arquivado e posteriormente
desarquivado neste período de 30 dias, ele contará como finalizado neste
componente.

As regras de negócio definidas para os Finalizados de Tutela são as
seguintes:

+-----------------------------------+-----------------------------------+
| tppr_dk                           | hierarquia                        |
+===================================+===================================+
| 6015                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual)                       |
+-----------------------------------+-----------------------------------+
| 6016                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual)       |
+-----------------------------------+-----------------------------------+
| 6017                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Extinção da            |
|                                   | Punibilidade por Outros           |
|                                   | Fundamentos                       |
+-----------------------------------+-----------------------------------+
| 6018                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Ausência/Insuficiência |
|                                   | de Provas (Falta de Suporte       |
|                                   | Fático Probatório)                |
+-----------------------------------+-----------------------------------+
| 6019                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Em razão de o          |
|                                   | adolescente ter alcançado a       |
|                                   | maioridade penal                  |
+-----------------------------------+-----------------------------------+
| 6020                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Extinção da             |
|                                   | Punibilidade por Outros           |
|                                   | Fundamentos                       |
+-----------------------------------+-----------------------------------+
| 6021                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Ausência/Insuficiência  |
|                                   | de Provas (Falta de Suporte       |
|                                   | Fático Probatório)                |
+-----------------------------------+-----------------------------------+
| 6022                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Em razão de o           |
|                                   | adolescente ter alcançado a       |
|                                   | maioridade penal                  |
+-----------------------------------+-----------------------------------+
| 6251                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Petição Inicial                   |
+-----------------------------------+-----------------------------------+
| 6324                              | MEMBRO > Arquivamento             |
+-----------------------------------+-----------------------------------+
| 6325                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior      |
+-----------------------------------+-----------------------------------+
| 6326                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral com TAC                  |
+-----------------------------------+-----------------------------------+
| 6327                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva)                         |
+-----------------------------------+-----------------------------------+
| 6328                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva)         |
+-----------------------------------+-----------------------------------+
| 6329                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário       |
+-----------------------------------+-----------------------------------+
| 6330                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial                           |
+-----------------------------------+-----------------------------------+
| 6331                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Desconhecimento do      |
|                                   | Autor                             |
+-----------------------------------+-----------------------------------+
| 6332                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Inexistência de Crime   |
+-----------------------------------+-----------------------------------+
| 6333                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Prescrição              |
+-----------------------------------+-----------------------------------+
| 6334                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Decadência              |
+-----------------------------------+-----------------------------------+
| 6335                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Retratação Lei Maria da |
|                                   | Penha                             |
+-----------------------------------+-----------------------------------+
| 6336                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Pagamento de Débito     |
|                                   | Tributário                        |
+-----------------------------------+-----------------------------------+
| 6337                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral                          |
+-----------------------------------+-----------------------------------+
| 6338                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Desconhecimento do     |
|                                   | Autor                             |
+-----------------------------------+-----------------------------------+
| 6339                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Inexistência de Crime  |
+-----------------------------------+-----------------------------------+
| 6340                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Prescrição             |
+-----------------------------------+-----------------------------------+
| 6341                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Decadência             |
+-----------------------------------+-----------------------------------+
| 6342                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Retratação Lei Maria   |
|                                   | da Penha                          |
+-----------------------------------+-----------------------------------+
| 6343                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Pagamento de Débito    |
|                                   | Tributário                        |
+-----------------------------------+-----------------------------------+
| 6344                              | MEMBRO > Arquivamento > Sem       |
|                                   | remessa ao Conselho               |
|                                   | Superior/Câmara                   |
+-----------------------------------+-----------------------------------+
| 6345                              | MEMBRO > Arquivamento > Sem       |
|                                   | remessa ao Conselho               |
|                                   | Superior/Câmara > Parcial         |
+-----------------------------------+-----------------------------------+
| 6346                              | MEMBRO > Arquivamento > Sem       |
|                                   | remessa ao Conselho               |
|                                   | Superior/Câmara > Integral        |
+-----------------------------------+-----------------------------------+
| 6350                              | MEMBRO > Homologação de           |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 6548                              | MEMBRO > Termo de reconhecimento  |
|                                   | de paternidade                    |
+-----------------------------------+-----------------------------------+
| 6553                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Insuficiência de       |
|                                   | Provas                            |
+-----------------------------------+-----------------------------------+
| 6591                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Falta de condições     |
|                                   | para o regular exercício do       |
|                                   | direito de ação                   |
+-----------------------------------+-----------------------------------+
| 6593                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Falta de condições para |
|                                   | o exercício do direito de ação    |
+-----------------------------------+-----------------------------------+
| 6644                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Resolução da questão  |
+-----------------------------------+-----------------------------------+
| 6645                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Não configuração de ilícito       |
+-----------------------------------+-----------------------------------+
| 6655                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Com   |
|                                   | TAC                               |
+-----------------------------------+-----------------------------------+
| 6656                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC                               |
+-----------------------------------+-----------------------------------+
| 6657                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Resolução da questão        |
+-----------------------------------+-----------------------------------+
| 6658                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos > Não    |
|                                   | configuração de ilícito           |
+-----------------------------------+-----------------------------------+
| 6659                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos >        |
|                                   | Inveracidade do fato              |
+-----------------------------------+-----------------------------------+
| 6660                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos >        |
|                                   | Prescrição                        |
+-----------------------------------+-----------------------------------+
| 6661                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos > Perda  |
|                                   | do objeto sem resolução da        |
|                                   | questão                           |
+-----------------------------------+-----------------------------------+
| 6662                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos > Falta  |
|                                   | de uma das condições da ação      |
+-----------------------------------+-----------------------------------+
| 6663                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos > Outros |
+-----------------------------------+-----------------------------------+
| 6664                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Resolução da        |
|                                   | questão                           |
+-----------------------------------+-----------------------------------+
| 6665                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Não configuração de |
|                                   | ilícito                           |
+-----------------------------------+-----------------------------------+
| 6666                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Inveracidade do     |
|                                   | fato                              |
+-----------------------------------+-----------------------------------+
| 6667                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Perda do objeto sem |
|                                   | resolução da questão              |
+-----------------------------------+-----------------------------------+
| 6668                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Falta de uma das    |
|                                   | condições da ação                 |
+-----------------------------------+-----------------------------------+
| 6669                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Outros              |
+-----------------------------------+-----------------------------------+
| 6670                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Com |
|                                   | TAC                               |
+-----------------------------------+-----------------------------------+
| 6671                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC                               |
+-----------------------------------+-----------------------------------+
| 6672                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Resolução da questão        |
+-----------------------------------+-----------------------------------+
| 6673                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Não configuração de ilícito |
+-----------------------------------+-----------------------------------+
| 6674                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Inveracidade do fato        |
+-----------------------------------+-----------------------------------+
| 6675                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Perda do objeto sem         |
|                                   | resolução da questão              |
+-----------------------------------+-----------------------------------+
| 6676                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Falta de uma das condições  |
|                                   | da ação                           |
+-----------------------------------+-----------------------------------+
| 6677                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela individual) > Sem |
|                                   | TAC > Outros                      |
+-----------------------------------+-----------------------------------+
| 6678                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Inveracidade do fato              |
+-----------------------------------+-----------------------------------+
| 6679                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Prescrição                        |
+-----------------------------------+-----------------------------------+
| 6680                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Perda do objeto sem resolução da  |
|                                   | questão                           |
+-----------------------------------+-----------------------------------+
| 6681                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Falta de uma das condições da     |
|                                   | ação                              |
+-----------------------------------+-----------------------------------+
| 6682                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Outros                            |
+-----------------------------------+-----------------------------------+
| 7737                              | SERVIDOR > Atualização da fase    |
|                                   | para “Finalizado” em decorrência  |
|                                   | da vinculação como juntada        |
+-----------------------------------+-----------------------------------+
| 7745                              | MEMBRO > Arquivamento > De        |
|                                   | notícia de fato ou procedimento   |
|                                   | de atribuição originária do PGJ   |
+-----------------------------------+-----------------------------------+
| 7834                              | MEMBRO > Indeferimento de pedido  |
|                                   | de desarquivamento                |
+-----------------------------------+-----------------------------------+
| 7869                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos    |
+-----------------------------------+-----------------------------------+
| 7870                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Parcial (Tutela coletiva) > Sem   |
|                                   | TAC > Por Outros Motivos          |
+-----------------------------------+-----------------------------------+
| 7871                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Morte do Agente        |
+-----------------------------------+-----------------------------------+
| 7872                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Morte de Agente         |
+-----------------------------------+-----------------------------------+
| 7912                              | MEMBRO > Arquivamento > Com       |
|                                   | Remessa ao PRE/PGE                |
+-----------------------------------+-----------------------------------+

Inquéritos (PIP)
^^^^^^^^^^^^^^^^

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em
andamento, e que não foram cancelados, das seguintes classes:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 3                                 | PROCESSO MILITAR > PROCESSO       |
|                                   | CRIMINAL > Procedimentos          |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial Militar                  |
+-----------------------------------+-----------------------------------+
| 494                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial                          |
+-----------------------------------+-----------------------------------+

PICs (PIP)
^^^^^^^^^^

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em
andamento, e que não foram cancelados, das seguintes classes:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 590                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Procedimento    |
|                                   | Investigatório Criminal (PIC-MP)  |
+-----------------------------------+-----------------------------------+

AISPs (PIP)
^^^^^^^^^^^

Esta Caixinha é para uso apenas de PIPs. Ela busca os documentos em
andamento, e que não foram cancelados, para todas as promotorias
pertencentes à AISP da promotoria sendo analisada, das seguintes
classes:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 3                                 | PROCESSO MILITAR > PROCESSO       |
|                                   | CRIMINAL > Procedimentos          |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial Militar                  |
+-----------------------------------+-----------------------------------+
| 494                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial                          |
+-----------------------------------+-----------------------------------+
| 590                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Procedimento    |
|                                   | Investigatório Criminal (PIC-MP)  |
+-----------------------------------+-----------------------------------+

Finalizados (PIP)
^^^^^^^^^^^^^^^^^

Esta Caixinha é para uso apenas de PIPs.

Da mesma forma que a da Tutela, ela busca os documentos que tiveram pelo
menos um andamento finalizador, dentro de regras de andamento definidas.
Os andamentos (e o documento correspondente) não podem ter sido
cancelados.

Além disso, a contagem é feita apenas para andamentos que ocorreram nos
últimos 30 dias.

Desarquivamentos *não* são levados em consideração no cálculo. Isso quer
dizer que, caso um documento seja arquivado e posteriormente
desarquivado neste período de 30 dias, ele contará como finalizado neste
componente.

As regras de negócio definidas para os Finalizados de PIP são as
seguintes:

+-----------------------------------+-----------------------------------+
| tppr_dk                           | hierarquia                        |
+===================================+===================================+
| 6017                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Extinção da            |
|                                   | Punibilidade por Outros           |
|                                   | Fundamentos                       |
+-----------------------------------+-----------------------------------+
| 6018                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Ausência/Insuficiência |
|                                   | de Provas (Falta de Suporte       |
|                                   | Fático Probatório)                |
+-----------------------------------+-----------------------------------+
| 6019                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Em razão de o          |
|                                   | adolescente ter alcançado a       |
|                                   | maioridade penal                  |
+-----------------------------------+-----------------------------------+
| 6253                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia > Escrita                |
+-----------------------------------+-----------------------------------+
| 6272                              | MEMBRO > Aditamento > Denúncia    |
+-----------------------------------+-----------------------------------+
| 6338                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Desconhecimento do     |
|                                   | Autor                             |
+-----------------------------------+-----------------------------------+
| 6339                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Inexistência de Crime  |
+-----------------------------------+-----------------------------------+
| 6340                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Prescrição             |
+-----------------------------------+-----------------------------------+
| 6341                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Decadência             |
+-----------------------------------+-----------------------------------+
| 6342                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Retratação Lei Maria   |
|                                   | da Penha                          |
+-----------------------------------+-----------------------------------+
| 6343                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Pagamento de Débito    |
|                                   | Tributário                        |
+-----------------------------------+-----------------------------------+
| 6346                              | MEMBRO > Arquivamento > Sem       |
|                                   | remessa ao Conselho               |
|                                   | Superior/Câmara > Integral        |
+-----------------------------------+-----------------------------------+
| 6350                              | MEMBRO > Homologação de           |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 6359                              | MEMBRO > Decisão Artigo 28 CPP /  |
|                                   | 397 CPPM > Confirmação Integral > |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 6361                              | MEMBRO > Proposta de transação    |
|                                   | penal                             |
+-----------------------------------+-----------------------------------+
| 6362                              | MEMBRO > Proposta de suspensão    |
|                                   | condicional do processo           |
+-----------------------------------+-----------------------------------+
| 6377                              | MEMBRO > Ciência > Sentença >     |
|                                   | Extintiva pela prescrição         |
+-----------------------------------+-----------------------------------+
| 6378                              | MEMBRO > Ciência > Sentença >     |
|                                   | Extintiva por outras causas       |
+-----------------------------------+-----------------------------------+
| 6392                              | MEMBRO > Ciência > Arquivamento   |
+-----------------------------------+-----------------------------------+
| 6436                              | MEMBRO > Ratificação de Denúncia  |
+-----------------------------------+-----------------------------------+
| 6524                              | SERVIDOR > Arquivamento           |
+-----------------------------------+-----------------------------------+
| 6591                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Falta de condições     |
|                                   | para o regular exercício do       |
|                                   | direito de ação                   |
+-----------------------------------+-----------------------------------+
| 6625                              | SERVIDOR > Informação sobre       |
|                                   | ajuizamento do documento no Poder |
|                                   | Judiciário                        |
+-----------------------------------+-----------------------------------+
| 6669                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | individual) > Outros              |
+-----------------------------------+-----------------------------------+
| 6682                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Conselho Superior >    |
|                                   | Integral sem TAC (Tutela          |
|                                   | coletiva) > Por Outros Motivos >  |
|                                   | Outros                            |
+-----------------------------------+-----------------------------------+
| 6718                              | SERVIDOR > Informação sobre o     |
|                                   | encaminhamento a Juízo para       |
|                                   | juntada a processo judicial       |
+-----------------------------------+-----------------------------------+
| 7737                              | SERVIDOR > Atualização da fase    |
|                                   | para “Finalizado” em decorrência  |
|                                   | da vinculação como juntada        |
+-----------------------------------+-----------------------------------+
| 7745                              | MEMBRO > Arquivamento > De        |
|                                   | notícia de fato ou procedimento   |
|                                   | de atribuição originária do PGJ   |
+-----------------------------------+-----------------------------------+
| 7811                              | SERVIDOR > Finalização de         |
|                                   | processo judicial                 |
+-----------------------------------+-----------------------------------+
| 7834                              | MEMBRO > Indeferimento de pedido  |
|                                   | de desarquivamento                |
+-----------------------------------+-----------------------------------+
| 7871                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Morte do Agente        |
+-----------------------------------+-----------------------------------+
| 7915                              | MEMBRO > Acordo de Não Persecução |
|                                   | Penal > Oferecimento de acordo    |
+-----------------------------------+-----------------------------------+

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Endpoint:

::

   GET /dominio/suamesa/documentos/<str:orgao_id>?tipo=tipo_de_dado&cpf=1234

   CPF é obrigatório apenas para alguns tipos de dado (ver lista abaixo).

   Tipos aceitos:
   - vistas: Vistas abertas para um órgão e CPF. (cpf obrigatório)
   - tutela_investigacoes: Número de investigações em curso de uma tutela.
   - tutela_processos: Número de processos em juízo de uma tutela.
   - tutela_finalizados: Número de documentos finalizados nos últimos 30 dias em uma tutela.
   - pip_inqueritos: Número de inquéritos ativos em uma PIP.
   - pip_pics: Número de PICs ativas em uma PIP.
   - pip_aisp: Número de inquéritos e PICs ativos na AISP de uma PIP.
   - pip_finalizados: Número de documentos finalizados nos últimos 30 dias para PIPs.

::

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
       "nr_documentos": 1
   }

O Sua Mesa Caixinhas é organizado em uma estrutura de Factory, por meio
de um DAO (Data Access Object). Isso quer dizer que as requisições são
feitas para um único endpoint/View, que se encarregará de repassá-la
para um DAO que decidirá qual função chamar para obter o dado do tipo
enviado no request.

Este DAO também se encarrega de verificar que o request veio com o
parâmetro de tipo definido, e que existe uma função para buscar o tipo
requisitado.

As regras de negócio explicadas na seção User Manual estão contidas
dentro destas funções correspondentes a cada tipo de dado.

Estes dados são buscados diretamente no Oracle (por meio da ORM do
Django). Isso quer dizer que, além dos cálculos serem realizados em
tempo real, não há processos adicionais sendo realizados no BDA para
este componente (criação ou uso de tabelas, por exemplo).

As queries ao Oracle estão todas definidas no script managers.py, e se
encarregam apenas de receber os parâmetros necessários para um
determinado cálculo.

Isso é útil para evitar a repetição de certos processamentos.

Por exemplo, os tipos de dados de Investigações (Tutela), Inquéritos
(PIP) e PICs (PIP) são essencialmente os mesmos - buscar documentos
ativos de certas classes. Por isso, os 3 fazem uso da mesma query
definida no managers.py (documentos.investigacoes.em_curso).

Dependências
~~~~~~~~~~~~

Não há dependências de tabelas (a não ser as do Oracle).

Troubleshooting
~~~~~~~~~~~~~~~

Como este componente não possui nenhum processo relacionado ou acesso de
tabelas no BDA, quaisquer problemas que possam surgir estarão
obrigatoriamente no backend (ou nos dados vindos do Oracle).

-  O endpoint está retornando algum dado? Com os nomes de atributo
   corretos na resposta? Se o dado está sendo retornado corretamente, o
   problema pode estar no Front.
-  Caso o dado esteja vindo com um número diferente do que deveria:

   -  Se for vistas abertas, o CPF está correto? Se sim, é possível que
      aquele CPF não esteja com vistas abertas no banco. Rodar a query
      de vistas abertas dada mais acima no BDA (ou diretamente no
      Oracle) pode ajudar a descobrir o problema.
   -  Se o problema for em outro tipo de dado, é possível que os
      documentos estejam sendo registrados com outras classes (ou os
      andamentos, no caso de Finalizados). Neste caso, as seguintes
      queries podem ajudar:

Para verificar os tipos de andamentos que apareceram nos últimos 30 dias
para um dado órgão:

::

   SELECT stao_tppr_dk, hierarquia, COUNT(1)
   FROM exadata_dev.mcpr_vista
   JOIN exadata_dev.mcpr_andamento ON vist_dk = pcao_vist_dk
   JOIN exadata_dev.mcpr_sub_andamento ON stao_pcao_dk = pcao_dk
   JOIN exadata_aux_dev.mmps_tp_andamento ON id = stao_tppr_dk
   WHERE vist_orgi_orga_dk = 400551
   AND pcao_dt_andamento >= days_sub(current_timestamp(), 30)
   GROUP BY stao_tppr_dk, hierarquia
   ORDER BY stao_tppr_dk;

Para verificar as classes de documentos ativos atualmente em um dado
órgão:

::

   SELECT docu_cldc_dk, hierarquia, COUNT(1)
   FROM exadata_dev.mcpr_documento
   JOIN exadata_aux_dev.mmps_classe_docto ON id = docu_cldc_dk
   WHERE docu_orgi_orga_dk_responsavel = 400551
   AND docu_tpst_dk != 11
   AND docu_fsdc_dk = 1
   GROUP BY docu_cldc_dk, hierarquia
   ORDER BY docu_cldc_dk;

Sua Mesa Detalhe
----------------

.. _user-manual-1:

User Manual
~~~~~~~~~~~

O Sua Mesa Detalhe corresponde à parte inferior do Sua Mesa, que mostra
os detalhes relacionados a cada uma das Caixinhas.

Há, porém, algumas exceções importantes de esclarecer. Primeiramente, a
Caixinhas de Finalizados não possui detalhe. E segundo, o detalhe de
vistas abertas, por fugir do padrão dos outros tipos de detalhe, é
calculado em um endpoint separado (e por isso tem sua própria seção
separada, mais abaixo).

Dito isso, existem 5 tipos de detalhe definidos neste componente:

-  Detalhe Investigações (Tutela)
-  Detalhe Processos (Tutela)
-  Detalhe Inquéritos (PIP)
-  Detalhe PICs (PIP)
-  Detalhe AISPs (PIP)

Vamos falar sobre eles individualmente.

Detalhe Investigações (Tutela)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: figuras/sua_mesa_detalhe_investigacoes.png
   :alt: title

   title

!! Tem um bug no ranking, não está mostrando reduções, e sim aumentos!

Este detalhe mostra simplesmente a variação do acervo de investigações
de um Tutela Coletiva. A janela de comparação é o mês corrente x o mês
anterior até o mesmo dia do mês (ou mais próximo).

Também há um ranking das promotorias com maiores variações do acervo.

As regras de negócio utilizadas para definir acervo são as mesmas da
Caixinha de Investigações (Tutela). No entanto, elas são definidas
novamente no código deste componente, de forma que faz sentido
repeti-las aqui:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 395                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Preparatório    |
+-----------------------------------+-----------------------------------+
| 392                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Inquérito Civil              |
+-----------------------------------+-----------------------------------+
| 51223                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | tutela de interesses individuais  |
|                                   | indisponíveis                     |
+-----------------------------------+-----------------------------------+
| 51222                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | outras atividades não sujeitas a  |
|                                   | inquérito civil                   |
+-----------------------------------+-----------------------------------+
| 51220                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Políticas       |
|                                   | Públicas                          |
+-----------------------------------+-----------------------------------+
| 51221                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de TAC             |
+-----------------------------------+-----------------------------------+
| 51219                             | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Procedimento Administrativo  |
|                                   | > Procedimento Administrativo de  |
|                                   | acompanhamento de Instituições    |
+-----------------------------------+-----------------------------------+

Detalhe Processos (Tutela)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: figuras/sua_mesa_detalhe_processos.png
   :alt: title

   title

Número de ajuizamentos de ação que ocorreram nos períodos indicados (em
número de dias correntes), para documentos não-cancelados, cuja vista do
andamento tenha sido aberta para o órgão. Ajuizamento de ação é definido
pela seguinte regra de andamento:

+---------+------------------------------------------------+
| tppr_dk | hierarquia                                     |
+=========+================================================+
| 6251    | MEMBRO > Ajuizamento de Ação > Petição Inicial |
+---------+------------------------------------------------+

O aumento nos últimos 12 meses é calculado comparando o número de
ajuizamentos nos últimos 360 dias correntes x 360 dias anteriores.

Para que estes dados sejam calculados para o órgão, ele necessariamente
deve ter um pacote de atribuição definido na tabela
``ATUALIZACAO_PJ_PACOTE``.

Detalhe Inquéritos (PIP)
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: figuras/sua_mesa_detalhe_inqueritos_pip.png
   :alt: title

   title

Este detalhe mostra diversas informações sobre os inquéritos que
passaram por uma PIP e CPF. São elas:

-  **Inquéritos que passaram pelo promotor** (ou seja, que tiveram vista
   aberta), no mês corrente. Aqui, um inquérito é contado apenas uma
   vez.
-  Número de **aberturas de vistas** total destes inquéritos. Aqui, se
   um inquérito tiver tido 2 vistas abertas, ele será contado 2 vezes.
-  Número de **aproveitamentos**, ou seja, número de inquéritos que
   tiveram denúncias, cautelares ou arquivamentos realizados. A contagem
   é por documento, não por andamento. De forma que se um inquérito
   tiver vários andamentos desses tipos, ele é contado apenas uma vez.
-  Porcentagem de aumento dos aproveitamentos, mês corrente x mês
   anterior até o mesmo dia.

Lembrando que estes dados são relativos ao **órgão e CPF**.

Também há dois rankings das promotorias:

-  Maiores volumes: É um ranking do número de inquéritos distintos que
   tiveram vistas abertas no órgão, no mês corrente.
-  Maiores aproveitamentos: É um ranking de número de inquéritos que
   tiveram aproveitamentos, no mês corrente.

Nos rankings, os dados são agregados por **órgão**.

As regras de negócio utilizadas para definir inquéritos são as mesmas da
Caixinha de Inquéritos (PIP). No entanto, elas são definidas novamente
no código deste componente, de forma que faz sentido repeti-las aqui:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 3                                 | PROCESSO MILITAR > PROCESSO       |
|                                   | CRIMINAL > Procedimentos          |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial Militar                  |
+-----------------------------------+-----------------------------------+
| 494                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Inquérito       |
|                                   | Policial                          |
+-----------------------------------+-----------------------------------+

Além disso, também há as regras usadas para definir aproveitamentos:

+-----------------------------------+-----------------------------------+
| tppr_dk                           | hierarquia                        |
+===================================+===================================+
| 1030                              | Propositura de medida cautelar    |
|                                   | autônoma                          |
+-----------------------------------+-----------------------------------+
| 1201                              | Oferecimento de denúncia          |
+-----------------------------------+-----------------------------------+
| 1202                              | Oferecimento de denúncia com      |
|                                   | pedido de prisão                  |
+-----------------------------------+-----------------------------------+
| 1208                              | Manifestação em medida cautelar   |
|                                   | requerida pela autoridade         |
|                                   | policial                          |
+-----------------------------------+-----------------------------------+
| 6017                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Extinção da            |
|                                   | Punibilidade por Outros           |
|                                   | Fundamentos                       |
+-----------------------------------+-----------------------------------+
| 6018                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Ausência/Insuficiência |
|                                   | de Provas (Falta de Suporte       |
|                                   | Fático Probatório)                |
+-----------------------------------+-----------------------------------+
| 6020                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Extinção da             |
|                                   | Punibilidade por Outros           |
|                                   | Fundamentos                       |
+-----------------------------------+-----------------------------------+
| 6038                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Interceptação  |
|                                   | Telefônica                        |
+-----------------------------------+-----------------------------------+
| 6039                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Interceptação  |
|                                   | de Dados Telemáticos              |
+-----------------------------------+-----------------------------------+
| 6040                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Obtenção de    |
|                                   | Dados Cadastrais                  |
+-----------------------------------+-----------------------------------+
| 6041                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Quebra de      |
|                                   | Sigilo Bancário                   |
+-----------------------------------+-----------------------------------+
| 6042                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Quebra de      |
|                                   | Sigilo Fiscal                     |
+-----------------------------------+-----------------------------------+
| 6043                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Outros Requerimentos |
|                                   | de Natureza Cautelar              |
+-----------------------------------+-----------------------------------+
| 6252                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia                          |
+-----------------------------------+-----------------------------------+
| 6253                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia > Escrita                |
+-----------------------------------+-----------------------------------+
| 6254                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Denúncia > Oral                   |
+-----------------------------------+-----------------------------------+
| 6257                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar)                        |
+-----------------------------------+-----------------------------------+
| 6258                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Protetiva                  |
+-----------------------------------+-----------------------------------+
| 6338                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Desconhecimento do     |
|                                   | Autor                             |
+-----------------------------------+-----------------------------------+
| 6339                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Inexistência de Crime  |
+-----------------------------------+-----------------------------------+
| 6340                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Prescrição             |
+-----------------------------------+-----------------------------------+
| 6341                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Decadência             |
+-----------------------------------+-----------------------------------+
| 6342                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Retratação Lei Maria   |
|                                   | da Penha                          |
+-----------------------------------+-----------------------------------+
| 6343                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Pagamento de Débito    |
|                                   | Tributário                        |
+-----------------------------------+-----------------------------------+
| 6346                              | MEMBRO > Arquivamento > Sem       |
|                                   | remessa ao Conselho               |
|                                   | Superior/Câmara > Integral        |
+-----------------------------------+-----------------------------------+
| 6350                              | MEMBRO > Homologação de           |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 6359                              | MEMBRO > Decisão Artigo 28 CPP /  |
|                                   | 397 CPPM > Confirmação Integral > |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 6367                              | MEMBRO > Requerimento de Prisão > |
|                                   | Preventiva > Preventiva - Art.    |
|                                   | 312 CPP                           |
+-----------------------------------+-----------------------------------+
| 6368                              | MEMBRO > Requerimento de Prisão > |
|                                   | Preventiva > Preventiva - Art.    |
|                                   | 366 CPP                           |
+-----------------------------------+-----------------------------------+
| 6369                              | MEMBRO > Requerimento de Prisão > |
|                                   | Preventiva > Preventiva - Art.    |
|                                   | 255 CPPM                          |
+-----------------------------------+-----------------------------------+
| 6370                              | MEMBRO > Requerimento de Prisão > |
|                                   | Temporária                        |
+-----------------------------------+-----------------------------------+
| 6392                              | MEMBRO > Ciência > Arquivamento   |
+-----------------------------------+-----------------------------------+
| 6549                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Centro de Apoio        |
|                                   | Operacional das Promotorias       |
|                                   | Eleitorais  CAO Eleitoral (EN    |
|                                   | 30-CSMP)                          |
+-----------------------------------+-----------------------------------+
| 6591                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Falta de condições     |
|                                   | para o regular exercício do       |
|                                   | direito de ação                   |
+-----------------------------------+-----------------------------------+
| 6593                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Parcial > Falta de condições para |
|                                   | o exercício do direito de ação    |
+-----------------------------------+-----------------------------------+
| 6620                              | MEMBRO > Requerimento de Prisão > |
|                                   | Preventiva > Preventiva - Art.    |
|                                   | 310, II, CPP (conversão)          |
+-----------------------------------+-----------------------------------+
| 6648                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais)      |
+-----------------------------------+-----------------------------------+
| 6649                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Interceptação Telefônica       |
+-----------------------------------+-----------------------------------+
| 6650                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Interceptação de Dados         |
|                                   | Telemáticos                       |
+-----------------------------------+-----------------------------------+
| 6651                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Obtenção de Dados Cadastrais   |
+-----------------------------------+-----------------------------------+
| 6652                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Quebra de Sigilo Bancário      |
+-----------------------------------+-----------------------------------+
| 6653                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Quebra de Sigilo Fiscal        |
+-----------------------------------+-----------------------------------+
| 6654                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Outros Requerimentos de Natureza  |
|                                   | Cautelar (não incidentais)        |
+-----------------------------------+-----------------------------------+
| 7745                              | MEMBRO > Arquivamento > De        |
|                                   | notícia de fato ou procedimento   |
|                                   | de atribuição originária do PGJ   |
+-----------------------------------+-----------------------------------+
| 7815                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar de Busca e        |
|                                   | Apreensão                         |
+-----------------------------------+-----------------------------------+
| 7816                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | de Busca e Apreensão              |
+-----------------------------------+-----------------------------------+
| 7871                              | MEMBRO > Arquivamento > Com       |
|                                   | remessa ao Poder Judiciário >     |
|                                   | Integral > Morte do Agente        |
+-----------------------------------+-----------------------------------+
| 7877                              | MEMBRO > Medida Incidental        |
|                                   | (cautelar) > Requerimento de      |
|                                   | Medida Cautelar do Art. 319 CPP   |
+-----------------------------------+-----------------------------------+
| 7878                              | MEMBRO > Ajuizamento de Ação >    |
|                                   | Requerimento de Outras Medidas    |
|                                   | Cautelares (Não Incidentais) >    |
|                                   | Requerimento de Medida Cautelar   |
|                                   | do Art. 319 CPP                   |
+-----------------------------------+-----------------------------------+
| 7897                              | MEMBRO > Decisão Artigo 28 CPP /  |
|                                   | 397 CPPM > Confirmação Parcial >  |
|                                   | Arquivamento                      |
+-----------------------------------+-----------------------------------+
| 7912                              | MEMBRO > Arquivamento > Com       |
|                                   | Remessa ao PRE/PGE                |
+-----------------------------------+-----------------------------------+

Detalhe PICs (PIP)
^^^^^^^^^^^^^^^^^^

O detalhe das PICs é muito parecido com o detalhe dos inquéritos, com um
dado sobre número de instaurações a mais. Ou seja, ele possuirá os
seguintes dados:

-  **PICs que passaram pelo promotor** (ou seja, que tiveram vista
   aberta), no mês corrente. Aqui, um PIC é contado apenas uma vez.
-  Número de **instaurações** de PICs no mês corrente. Isso é calculado
   por meio da data de cadastro do documento na tabela. Ou seja, se um
   documento for cadastrado no sistema no mês corrente, ele contará como
   uma instauração.
-  Número de **aberturas de vistas** total destes PICs. Aqui, se um PIC
   tiver tido 2 vistas abertas, ele será contado 2 vezes.
-  Número de **aproveitamentos**, ou seja, número de PICs que tiveram
   denúncias, cautelares ou arquivamentos realizados. A contagem é por
   documento, não por andamento. De forma que se um inquérito tiver
   vários andamentos desses tipos, ele é contado apenas uma vez.
-  Porcentagem de aumento dos aproveitamentos, mês corrente x mês
   anterior até o mesmo dia.

A regra para definir PIC é a mesma da Caixinha de PICs:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 590                               | PROCESSO CRIMINAL > Procedimentos |
|                                   | Investigatórios > Procedimento    |
|                                   | Investigatório Criminal (PIC-MP)  |
+-----------------------------------+-----------------------------------+

Os andamentos definidos como aproveitamentos são os mesmos do Detalhe
Inquéritos acima.

Detalhe AISPs (PIP)
^^^^^^^^^^^^^^^^^^^

.. figure:: figuras/sua_mesa_detalhe_aisp_pip.png
   :alt: title

   title

O detalhe de AISPs mostra o aumento do número de procedimentos da AISP
do órgão em questão, no mês corrente x mês anterior até o mesmo dia.

Procedimentos são definidos juntando as regras de documentos usadas no
Detalhe Inquéritos e Detalhe PICs.

O ranking mostra, no mês corrente, as AISPs que possuem o maior número
de procedimentos.

.. _estrutura-do-código-1:

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Endpoint:

::

   GET /dominio/suamesa/documentos-detalhe/<str:orgao_id>?tipo=tipo_de_dado&cpf=1234&n=3&intervalo=30

   CPF (opcional) - depende do tipo de dado requisitado (ver lista abaixo).
   n (opcional) - Número de promotorias para retornar no Top N. Default: 3.
   intervalo (opcional) - Intervalo de tempo para olhar, caso disponível. Default: 30.

   Tipos aceitos:
   - tutela_investigacoes: Detalhe de investigações em curso de uma tutela.
   - tutela_processos: Detalhe de processos em juízo de uma tutela.
   - pip_inqueritos: Detalhe de inquéritos da PIP. (Requer CPF)
   - pip_pics: Detalhe de PICs da PIP. (Requer CPF)
   - pip_aisp: Detalhe de inquéritos e PICs da AISP de uma PIP.

::

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
       "metrics": {
           'dado1': 1234,
           'dado2': 1234,
       },
       "rankings": [
           {
               'ranking_fieldname': 'nome',
               'data': [{'nm_orgao': 'Orgao1', 'valor': 10}, {'nm_orgao': 'Orgao2', 'valor': 5}, ...]
           }
       ],
       "mapData: {}
   }

   O atributo 'valor' dos rankings pode vir como 'valor_percentual', caso seja relativo a uma porcentagem.

Processo no BDA cria essas tabelas:

-  tb_detalhe_processo
-  tb_detalhe_documentos_orgao
-  tb_detalhe_documentos_orgao_cpf

Elas são usadas para alimentar o backend.

Explicar a estrutura de DAO Factory, explicar a separação dos DAOs entre
DAO Metrics para a construção das frases de cima, e DAO Ranking para a
construção dos rankings. E explicitar a peculiaridade de certos casos,
como Tutela Processos e AISPs.

.. _dependências-1:

Dependências
~~~~~~~~~~~~

-  tb_pip_aisp
-  tb_acervo
-  atualizacao_pj_pacote
-  tabelas do exadata

.. _troubleshooting-1:

Troubleshooting
~~~~~~~~~~~~~~~

Sua Mesa Detalhe Vistas Abertas
-------------------------------

É composto por dois endpoints separados dos outros!
