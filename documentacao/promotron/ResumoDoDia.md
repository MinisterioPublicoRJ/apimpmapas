## Resumo Do Dia

O primeiro componente é o Resumo do Dia. Nele, são realizados cálculos para formar frases relativas ao status do dia atual.

![title](figuras/resumo_do_dia.png)

### Frase de Resolutividade

Esta frase indica, a porcentagem de promotorias de mesma atribuição que tiveram menos saídas do que a promotoria sendo analisada, nos últimos 30 dias correntes. Para explicar melhor:

<b>Mesma atribuição</b>:

O conceito de atribuição segue o que foi definido no arquivo README.md; na prática, para os tipos de promotorias definidos, isso quer dizer:

- Tutelas Coletivas: a atribuição diz respeito ao pacote de atribuição no qual a Tutela está inserida (Consumidor, Cidadania, etc).
- PIPs: a atribuição diz respeito a todas as PIPs Territoriais.

<b>Saídas</b>: <br>
São os andamentos finalizadores considerados como resolutivos. Os andamentos definidos no momento são:

- Tutelas Coletivas:

| tppr_dk | hierarquia |
| :- | :- |
| 6657 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Sem TAC > Resolução da questão |
| 6655 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Parcial (Tutela coletiva) > Com TAC |
| 6644 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral sem TAC (Tutela coletiva) > Resolução da questão |
| 6326 | MEMBRO > Arquivamento > Com remessa ao Conselho Superior > Integral com TAC |
| 6251 | MEMBRO > Ajuizamento de Ação > Petição Inicial |

- PIPs:

| tppr_dk | hierarquia |
| - | :- |
| 7922 | MEMBRO > Manifestação > Pela extinção da punibilidade > Em razão do cumprimento do Acordo de Não Persecução Penal |
| 7915 | MEMBRO > Acordo de Não Persecução Penal > Oferecimento de acordo |
| 7883 | MEMBRO > Acordo de Não Persecução Penal > Celebração de acordo |
| 7868 | MEMBRO > Colaboração Premiada |
| 7912 | MEMBRO > Arquivamento > Com Remessa ao PRE/PGE |
| 7897 | MEMBRO > Decisão Artigo 28 CPP / 397 CPPM > Confirmação Parcial > Arquivamento |
| 7928 | MEMBRO > Ciência > Homologação de Acordo de Não Persecução Penal |
| 7871 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Morte do Agente |
| 7917 | MEMBRO > Acordo de Não Persecução Penal > Pedido de homologação de acordo |
| 7914 | MEMBRO > Acordo de Não Persecução Penal |
| 7827 | MEMBRO > Despacho > Acordo Extrajudicial |
| 7745 | MEMBRO > Arquivamento > De notícia de fato ou procedimento de atribuição originária do PGJ |
| 6591 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Falta de condições para o regular exercício do direito de ação |
| 1201 | Oferecimento de denúncia |
| 1202 | Oferecimento de denúncia com pedido de prisão |
| 6017 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Extinção da Punibilidade por Outros Fundamentos |
| 6018 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Ausência/Insuficiência de Provas (Falta de Suporte Fático Probatório) |
| 6020 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Extinção da Punibilidade por Outros Fundamentos |
| 6252 | MEMBRO > Ajuizamento de Ação > Denúncia |
| 6253 | MEMBRO > Ajuizamento de Ação > Denúncia > Escrita |
| 6254 | MEMBRO > Ajuizamento de Ação > Denúncia > Oral |
| 6343 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Pagamento de Débito Tributário |
| 6346 | MEMBRO > Arquivamento > Sem remessa ao Conselho Superior/Câmara > Integral |
| 6350 | MEMBRO > Homologação de Arquivamento |
| 6359 | MEMBRO > Decisão Artigo 28 CPP / 397 CPPM > Confirmação Integral > Arquivamento |
| 6361 | MEMBRO > Proposta de transação penal |
| 6362 | MEMBRO > Proposta de suspensão condicional do processo |
| 6338 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Desconhecimento do Autor |
| 6339 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Inexistência de Crime |
| 6340 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Prescrição |
| 6341 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Decadência |
| 6342 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Integral > Retratação Lei Maria da Penha |
| 6391 | MEMBRO > Ciência > Suspensão do processo - Art. 366 CPP |
| 6392 | MEMBRO > Ciência > Arquivamento |
| 6549 | MEMBRO > Arquivamento > Com remessa ao Centro de Apoio Operacional das Promotorias Eleitorais  CAO Eleitoral (EN 30-CSMP) |
| 6593 | MEMBRO > Arquivamento > Com remessa ao Poder Judiciário > Parcial > Falta de condições para o exercício do direito de ação |

Utilizando estas regras, o cálculo é feito então contabilizando: 
- Os andamentos com data (pcao_dt_andamento) nos últimos 30 dias;
- Que não foram cancelados;
- Cujos documentos não foram cancelados;
- E Que sejam dos tipos definidos acima. 

Esta contagem é então utilizada para fazer um ranking com promotorias dentro da mesma atribuição, e saber a porcentagem de promotorias que tem contagem menor do que a promotoria que está sendo analisada.

As regras de andamentos finalizadores estão definidas na tabela <b>exadata_aux(_dev).tb_regra_negocio_saida</b> e podem ser modificadas caso uma mudança de regra de negócio ocorra. Esses andamentos são associados a cada pacote de atribuição, de forma que é possível ter regras para tutelas coletivas de cidadania, e regras diferentes para consumidor, por exemplo.

O script de cálculo pode ser encontrado em <b>scripts-bda/robo_promotoria/src/tabela_saida.py</b> e a tabela final é <b>exadata_aux(_dev).tb_saida</b> <br>
E a view no backend que utiliza a tabela gerada está em <b>apimpmapas/dominio/tutela/views.py -> SaidasView</b>

<font color="green">!! Apesar da frase dizer últimos 30 dias, parece que o script de criação da tabela atualmente considera últimos 60 dias.</font>

### Frase de Acervo

Esta frase pega o número de documentos ativos de determinadas classes para as promotorias dentro da mesma atribuição (no dia em que está sendo visto), e em seguida calcula um limite superior e inferior a partir do qual um dado volume não seria mais regular. Compara-se então o acervo da promotoria com estes limites para definir se ela está com um volume considerado regular ou não.

As classes de documentos utilizadas no momento são:

- Tutelas Coletivas:


| cldc_dk | hierarquia |
| :- | :- |
| 395 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Procedimento Preparatório |
| 392 | EXTRAJUDICIAIS > PROCEDIMENTOS DO MP > Inquérito Civil |

- PIPs:


| cldc_dk | hierarquia |
| :- | :- |
| 3 | PROCESSO MILITAR > PROCESSO CRIMINAL > Procedimentos Investigatórios > Inquérito Policial Militar |
| 494 | PROCESSO CRIMINAL > Procedimentos Investigatórios > Inquérito Policial |
| 590 | PROCESSO CRIMINAL > Procedimentos Investigatórios > Procedimento Investigatório Criminal (PIC-MP) |

Como no caso da frase de resolutividade, as regras das classes de documentos têm uma tabela própria, em <b>exadata_aux(_dev).tb_regra_negocio_investigacao</b>, e as classes a serem consideradas podem ser modificadas de uma atribuição a outra.

O script de cálculo para essa frase pode ser encontrado em <b>scripts-bda/robo_promotoria/src/tabela_distribuicao.py</b> e a tabela final é <b>exadata_aux(_dev).tb_distribuicao</b><br>
A view no backend é a <b>apimpmapas/dominio/tutela/views.py -> OutliersView</b>

### Frase de Entradas

A última frase é relativa ao número de vistas abertas em um determinado dia, e indica se o número de vistas em um determinado dia está dentro ou fora do padrão. A ideia é muito parecida com a Frase de Acervo, mas ao invés de comparar acervo em relação à promotoria, comparam-se vistas abertas em relação ao histórico do promotor naquela promotoria.<br>

<font color="green">!! Queremos comparar sempre dentro do mesmo CPF? Ou queremos comparar com o órgão inteiro?</font>

O cálculo é feito pegando as vistas que foram abertas em cada dia, nos últimos 60 dias, excluindo sábados e domingos. Também não são consideradas as vistas relativas a documentos cancelados. Com isso, é possível calcular a partir de quantas vistas (ou de quão poucas vistas) um dia é muito diferente dos outros. Limites superior e inferior, como do caso do acervo.

Diferente das outras frases do Resumo do Dia, a Frase de Entradas não possui tabela de regras, já que todas as vistas são consideradas, independente da classe do documento ao qual elas se referem. <br>
O script de cálculo para essa frase pode ser encontrado em <b>scripts-bda/robo_promotoria/src/tabela_dist_entradas.py</b> e a tabela final é <b>exadata_aux(_dev).tb_dist_entradas</b> <br>
A view no backend é a <b>apimpmapas/dominio/tutela/views.py -> EntradasView</b>

## Troubleshooting

Caso alguma das frases apareça com valores estranhos, ou não apareça quando deveria aparecer, alguns pontos podem ser verificados rapidamente para encontrar possíveis erros:

- A promotoria sendo analisada tem pacote de atribuição definido na tabela exadata_aux(_dev).atualizacao_pj_pacote?
- Caso ela possua pacote de atribuição, existem regras de saídas definidas para o pacote dela na tabela tb_regra_negocio_saida e/ou tb_regra_negocio_investigacao (caso o problema seja na frase de resolutividade ou de acervo)?
- Se as regras estiverem definidas, verifique se a tabela gerada tem dados para aquela promotoria (ou promotoria e CPF, no caso da Frase de Entradas). Se a tabela estiver sem dados para aquela promotoria, o problema pode ser na geração da tabela no BDA, ou dos dados usados para gerá-las. Caso haja dados e eles não estejam aparecendo corretamente, pode ser um problema no backend.

A partir dessas perguntas, deve ficar mais fácil identificar a fonte do problema e analisá-lo.

