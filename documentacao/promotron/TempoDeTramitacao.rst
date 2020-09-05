Tempo de Tramitação
===================

.. contents:: :local:

.. figure:: figuras/tempo_tramitacao.png

   Componente de Tempo de Tramitação


User Manual
~~~~~~~~~~~

O componente de Tempo de Tramitação analisa diversas métricas relativas ao tempo de tramitação dos documentos de um dado órgão, sendo possível compará-las com outros órgãos do mesmo pacote.

O tempo de tramitação é definido como sendo o tempo entre a data de cadastro de um documento no sistema, até a data de um andamento considerado finalizador. Apenas documentos e andamentos que não foram cancelados são levados em consideração. Caso o documento possua mais de um andamento finalizador, é considerado o mais recente.

Neste componente, são definidos diversos conjuntos de regras - que incluem as classes de documentos a serem considerados; os tipos de andamento finalizadores; os pacotes para os quais a regra é válida; e um tempo mínimo que deve haver entre o cadastro e o andamento finalizador para que ele seja levado em consideração.

Atualmente, as seguintes regras são definidas:

Tutela Coletiva - Inquéritos Civis
----------------------------------

Nesta regra, são considerados os pacotes de Tutela Coletiva (pacotes de 20 a 33). O tempo mínimo entre o cadastro e o andamento finalizador deve ser de 5 dias. Finalizações que tenham ocorrido com menos de 5 dias são excluídas, pois são consideradas como um erro.

Classes de documentos consideradas:

+-----------------------------------+-----------------------------------+
| cldc_dk                           | hierarquia                        |
+===================================+===================================+
| 392                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
|                                   | MP > Inquérito Civil              |
+-----------------------------------+-----------------------------------+

Andamentos considerados como finalizadores:

+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tppr_dk | hierarquia                                                                                                                                                     |
+=========+================================================================================================================================================================+
| 6015    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual)                                                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6016    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual)                                                                         |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6017    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Extinção da Punibilidade por Outros Fundamentos                                           |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6018    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório)                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6019    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Em razão de o adolescente ter alcançado a maioridade penal                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6020    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Extinção da Punibilidade por Outros Fundamentos                                            |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6021    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório)                      |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6022    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Em razão de o adolescente ter alcançado a maioridade penal                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6251    | MEMBRO > Ajuizamento de Ação > Petição Inicial                                                                                                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6324    | MEMBRO > Arquivamento                                                                                                                                          |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6325    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior                                                                                                       |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6326    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral com TAC                                                                                    |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6327    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva)                                                                  |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6328    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva)                                                                           |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6329    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário                                                                                                        |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6330    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial                                                                                              |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6331    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Desconhecimento do Autor                                                                   |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6332    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Inexistência de Crime                                                                      |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6333    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Prescrição                                                                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6334    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Decadência                                                                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6335    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Retratação Lei Maria da Penha                                                              |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6336    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Pagamento de Débito Tributário                                                             |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6337    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral                                                                                             |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6338    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Desconhecimento do Autor                                                                  |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6339    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Inexistência de Crime                                                                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6340    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Prescrição                                                                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6341    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Decadência                                                                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6342    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Retratação Lei Maria da Penha                                                             |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6343    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Pagamento de Débito Tributário                                                            |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6344    | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara                                                                                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6345    | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Parcial                                                                                      |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6346    | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Integral                                                                                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6548    | MEMBRO > Termo de reconhecimento de paternidade                                                                                                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6553    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Insuficiência de Provas                                                                   |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6591    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Falta de condições para o regular exercício do direito de ação                            |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6593    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Falta de condições para o exercício do direito de ação                                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6644    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Resolução da questão                                           |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6645    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Não configuração de ilícito               |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6655    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Com TAC                                                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6656    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC                                                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6657    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Resolução da questão                                          |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6658    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Não configuração de ilícito              |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6659    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Inveracidade do fato                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6660    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Prescrição                               |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6661    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Perda do objeto sem resolução da questão |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6662    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Falta de uma das condições da ação       |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6663    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos > Outros                                   |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6664    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Resolução da questão                                         |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6665    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Não configuração de ilícito                                  |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6666    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Inveracidade do fato                                         |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6667    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Perda do objeto sem resolução da questão                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6668    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Falta de uma das condições da ação                           |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6669    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Outros                                                       |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6670    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Com TAC                                                               |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6671    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC                                                               |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6672    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Resolução da questão                                        |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6673    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Não configuração de ilícito                                 |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6674    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Inveracidade do fato                                        |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6675    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Perda do objeto sem resolução da questão                    |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6676    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Falta de uma das condições da ação                          |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6677    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela individual) > Sem TAC > Outros                                                      |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6678    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Inveracidade do fato                      |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6679    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Prescrição                                |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6680    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Perda do objeto sem resolução da questão  |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6681    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Falta de uma das condições da ação        |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 7745    | MEMBRO > Arquivamento > De notícia de fato ou procedimento de atribuição originária do PGJ                                                                     |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 6682    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Outros                                    |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 7869    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos                                             |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 7870    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Por Outros Motivos                                            |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 7871    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Morte do Agente                                                                           |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 7872    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Morte de Agente                                                                            |
+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------+



Tutela Coletiva - Ações até a Sentença
--------------------------------------

Nesta regra, são considerados os pacotes de Tutela Coletiva (pacotes de 20 a 33). O tempo mínimo entre o cadastro e o andamento finalizador deve ser de 5 dias. Finalizações que tenham ocorrido com menos de 5 dias são excluídas, pois são consideradas como um erro.

Classes de documentos consideradas:

+-----------------------------------+-----------------------------------+
| classe_documento                  | hierarquia                        |
+===================================+===================================+
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
| 441                               | JUIZADOS DA INFÂNCIA E DA         |
|                                   | JUVENTUDE > Seção Cível >         |
|                                   | Processo de Conhecimento > Ação   |
|                                   | Civil Pública                     |
+-----------------------------------+-----------------------------------+

Andamentos considerados como finalizadores:

+---------+-----------------------------------------------------------+
| tppr_dk | hierarquia                                                |
+---------+-----------------------------------------------------------+
| 6374    | MEMBRO > Ciência > Sentença > Favorável                   |
+---------+-----------------------------------------------------------+
| 6375    | MEMBRO > Ciência > Sentença > Desfavorável                |
+---------+-----------------------------------------------------------+
| 6376    | MEMBRO > Ciência > Sentença > Parcialmente favorável      |
+---------+-----------------------------------------------------------+
| 6377    | MEMBRO > Ciência > Sentença > Extintiva pela prescrição   |
+---------+-----------------------------------------------------------+
| 6378    | MEMBRO > Ciência > Sentença > Extintiva por outras causas |
+---------+-----------------------------------------------------------+

Tutela Coletiva - Ações até o trânsito em julgado
-------------------------------------------------

Nesta regra, são considerados os pacotes de Tutela Coletiva (pacotes de 20 a 33). O tempo mínimo entre o cadastro e o andamento finalizador deve ser de 5 dias. Finalizações que tenham ocorrido com menos de 5 dias são excluídas, pois são consideradas como um erro.

Classes de documentos consideradas:

+-----------------------------------+-----------------------------------+
| classe_documento                  | hierarquia                        |
+===================================+===================================+
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
| 441                               | JUIZADOS DA INFÂNCIA E DA         |
|                                   | JUVENTUDE > Seção Cível >         |
|                                   | Processo de Conhecimento > Ação   |
|                                   | Civil Pública                     |
+-----------------------------------+-----------------------------------+

Andamentos considerados como finalizadores:

+---------+---------------------------------------------+
| tppr_dk | hierarquia                                  |
+---------+---------------------------------------------+
| 6393    | MEMBRO > Ciência > Trânsito em Julgado      |
+---------+---------------------------------------------+
| 7811    | SERVIDOR > Finalização de processo judicial |
+---------+---------------------------------------------+

Ou, caso tenham ocorrido há mais do que 60 dias, estes andamentos também são considerados como finalizadores para trânsito em julgado:

+---------+-----------------------------------------------------------+
| tppr_dk | hierarquia                                                |
+---------+-----------------------------------------------------------+
| 6374    | MEMBRO > Ciência > Sentença > Favorável                   |
+---------+-----------------------------------------------------------+
| 6375    | MEMBRO > Ciência > Sentença > Desfavorável                |
+---------+-----------------------------------------------------------+
| 6376    | MEMBRO > Ciência > Sentença > Parcialmente favorável      |
+---------+-----------------------------------------------------------+
| 6377    | MEMBRO > Ciência > Sentença > Extintiva pela prescrição   |
+---------+-----------------------------------------------------------+
| 6378    | MEMBRO > Ciência > Sentença > Extintiva por outras causas |
+---------+-----------------------------------------------------------+
| 6380    | MEMBRO > Ciência > Acórdão > Favorável                    |
+---------+-----------------------------------------------------------+
| 6381    | MEMBRO > Ciência > Acórdão > Desfavorável                 |
+---------+-----------------------------------------------------------+
| 6382    | MEMBRO > Ciência > Acórdão > Parcialmente Favorável       |
+---------+-----------------------------------------------------------+
| 6383    | MEMBRO > Ciência > Acórdão > Extintiva pela Prescrição    |
+---------+-----------------------------------------------------------+
| 6384    | MEMBRO > Ciência > Acórdão > Extintiva por outras causas  |
+---------+-----------------------------------------------------------+

PIP - Investigações
-------------------

Nesta regra, são considerados os pacotes de PIPs (pacotes de 200 a 209). O tempo mínimo entre o cadastro e o andamento finalizador deve ser de 1 dia. Finalizações que tenham ocorrido no mesmo dia do cadastro são consideradas como erro, e excluídas do cálculo.

Classes de documentos consideradas:

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

Andamentos considerados como finalizadores:

+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| tppr_dk | hierarquia                                                                                                                                 |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6017    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Extinção da Punibilidade por Outros Fundamentos                       |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6018    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório) |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6019    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Em razão de o adolescente ter alcançado a maioridade penal            |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6253    | MEMBRO > Ajuizamento de Ação > Denúncia > Escrita                                                                                          |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6272    | MEMBRO > Aditamento > Denúncia                                                                                                             |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6338    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Desconhecimento do Autor                                              |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6339    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Inexistência de Crime                                                 |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6340    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Prescrição                                                            |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6341    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Decadência                                                            |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6342    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Retratação Lei Maria da Penha                                         |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6343    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Pagamento de Débito Tributário                                        |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6346    | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Integral                                                                 |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6359    | MEMBRO > Decisão Artigo 28 CPP / 397 CPPM > Confirmação Integral > Arquivamento                                                            |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6361    | MEMBRO > Proposta de transação penal                                                                                                       |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6362    | MEMBRO > Proposta de suspensão condicional do processo                                                                                     |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6377    | MEMBRO > Ciência > Sentença > Extintiva pela prescrição                                                                                    |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6378    | MEMBRO > Ciência > Sentença > Extintiva por outras causas                                                                                  |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6392    | MEMBRO > Ciência > Arquivamento                                                                                                            |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6436    | MEMBRO > Ratificação de Denúncia                                                                                                           |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6524    | SERVIDOR > Arquivamento                                                                                                                    |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6591    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Falta de condições para o regular exercício do direito de ação        |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6625    | SERVIDOR > Informação sobre ajuizamento do documento no Poder Judiciário                                                                   |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6669    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela individual) > Outros                                   |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6682    | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Por Outros Motivos > Outros                |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 6718    | SERVIDOR > Informação sobre o encaminhamento a Juízo para juntada a processo judicial                                                      |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 7737    | SERVIDOR > Atualização da fase para "Finalizado" em decorrência da vinculação como juntada                                                 |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 7745    | MEMBRO > Arquivamento > De notícia de fato ou procedimento de atribuição originária do PGJ                                                 |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 7811    | SERVIDOR > Finalização de processo judicial                                                                                                |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 7871    | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Morte do Agente                                                       |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| 7915    | MEMBRO > Acordo de Não Persecução Penal > Oferecimento de acordo                                                                           |
+---------+--------------------------------------------------------------------------------------------------------------------------------------------+

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
------------

::

   Nome da Tabela: TB_TEMPO_TRAMITACAO_INTEGRADO
   Colunas: 
      id_orgao (int)
      nome_regra (string)
      media_orgao (double)
      minimo_orgao (int)
      maximo_orgao (int)
      mediana_orgao (double)
      media_pacote (double)
      minimo_pacote (int)
      maximo_pacote (int)
      mediana_pacote (double)
    
O processo no BDA deste componente é separado em scripts auxiliares. O processo principal é definido no `Script Principal do Tempo de Tramitação`_. É neste script que as regras a serem calculadas são definidas, assim como os pacotes aos quais elas se aplicarão, as classes de documentos e andamentos a serem considerados, e o tempo mínimo de cada uma. Estas regras serão então passadas para uma função definida no `Script Auxiliar do Tempo de Tramitação`_, que se encarregará de fazer as consultas necessárias em banco, assim como os cálculos de média, mínimo, máximo e mediana dos tempos de tramitação dentro de cada órgão, e dentro de cada pacote considerado.

Uma segunda função auxiliar, específica das ações de Tutela Coletiva até o trânsito em julgado, também é chamada. Isso ocorre pois no caso específico do trânsito em julgado, há dois conjuntos de andamentos que devem ser tratados de forma diferenciada.

Os resultados finais então são concatenados em uma única tabela, onde a coluna ``nome_regra`` irá definir em relação a qual conjunto de regras uma linha se refere, e salvos na tabela final TB_TEMPO_TRAMITACAO_INTEGRADO. Elas estão definidas com os seguintes nomes:

- Tutela Inquéritos Civis: tutela_inqueritos_civis;
- Tutela Ações até a Sentença: tutela_acoes_sentenca;
- Tutela Ações até o Trânsito em Julgado: tutela_acoes_transito_julgado;
- PIP Investigações: pip_investigacoes

Uma pergunta que pode surgir é: por que essa tabela se chama TB_TEMPO_TRAMITACAO_INTEGRADO e não TB_TEMPO_TRAMITACAO? Isto ocorre porque, inicialmente, uma tabela TB_TEMPO_TRAMITACAO foi feita, mas ela contemplava todas as 3 regras associadas a Tutelas Coletivas conjuntamente (ou seja, cada linha na tabela possuia 24 colunas com valores estatísticos - 8 para inquéritos civis, 8 para ações até a sentença, e 8 para ações até o trânsito em julgado). Esse esquema, no entanto, tornava difícil adicionar novas regras. Para levar em consideração o tempo de tramitação de PIPs, por exemplo, seria necessário ou reformular a tabela, ou criar uma nova tabela. Foi decidido mudar a tabela (e a forma como ela era calculada) para torná-la mais genérica, e fácil de expandir.

É por este motivo também que, pode-se perceber, há outros dois scripts auxiliares na pasta de ``tramitacao``, além dos que estão explicitados aqui. Eles eram utilizados no formato antigo de tabela, mas não o são mais.

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tabela_tempo_tramitacao.py.
Script Auxiliar 1: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tramitacao/utils_tempo.py.
Script Auxiliar 2: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tramitacao/tutela_acoes.py.

.. _`Script Principal do Tempo de Tramitação`: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/develop/robo_promotoria/src/tabela_detalhe_documento.py

.. _`Script Auxiliar do Tempo de Tramitação`: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tramitacao/utils_tempo.py

View Backend
------------

::

   GET dominio/endpoint/

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
       "id_orgao": 1,
       "tp_tempo": "tutela_acoes",
       "media_orgao": 10.5,
       "minimo_orgao": 1,
       "maximo_orgao": 20,
       "mediana_orgao": 12,
       "media_pacote": 9.5,
       "minimo_pacote": 0,
       "maximo_pacote": 21,
       "mediana_pacote": 10.0
   }

A View no Backend irá simplesmente consultar a tabela no BDA, filtrando pelo órgão que está sendo analisada, e repassar os dados para o Frontend.

Atualmente, existe uma verificação de versão do endpoint, por meio de uma variável ``version`` que é passada no request. Se ``version=1.1``, a tabela TB_TEMPO_TRAMITACAO_INTEGRADO é utilizada. Senão, a tabela antiga TB_TEMPO_TRAMITACAO é a que é consultada.

A tendência é que a verificação de versão pare de ser feita, e toda chamada vá para a tabela integrada, que é a mais recente, e essa consulta à tabela antiga não seja mais feita, já que ela não é mais atualizada.

Nome da View: `TempoTramitacaoView`_.

.. _TempoTramitacaoView: https://github.com/MinisterioPublicoRJ/apimpmapas/blob/develop/dominio/tutela/views.py#L455

Dependências
~~~~~~~~~~~~

- :ref:`tabelas-auxiliares-atualizacao-pj-pacote`
- Tabelas Exadata

Troubleshooting
~~~~~~~~~~~~~~~

Verificar se tem pacote definido na tabela de pacotes.
Verificar na tabela TB_TEMPO_TRAMITACAO_INTEGRADO se o órgão em questão possui linhas referentes às regras definidas (caso seja um órgão de Tutela, deve possuir 3 linhas - uma para cada regra de Tutela. Caso seja uma PIP, deve possuir uma única linha, referente à pip investigações).
Caso esteja vindo vazio ainda assim, verificar que o órgão em questão tenha tido andamentos finalizadores em documentos das classes definidas na última semana.