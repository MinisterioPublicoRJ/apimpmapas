Alertas
=======

.. contents:: :local:

.. figure:: figuras/alertas.png

   Componente de Alertas

User Manual
~~~~~~~~~~~

O componente de alerta, como o nome já diz, serve para entregar alertas e notificações sobre assuntos de possível interesse do promotor, de maneira centralizada.

Os seguintes alertas estão implementados:

- Documentos com novas ITs do GATE;
- ICs sem prorrogação por mais de um ano;
- Documentos com vitimas recorrentes recebidos nos ultimos 30 dias;
- Ofício fora do prazo;
- Expedientes de Ouvidoria (EO) pendentes de recebimento;
- Procedimento Preparatório fora do prazo;
- PAs sem prorrogação por mais de um ano;
- Vistas abertas em documentos já fechados;
- Notícia de Fato a mais de 120 dias;
- Movimento em processo de segunda instância.
- Alertas de prescrição, divididos em 4 subtipos:
    -- Todos os crimes prescritos;
    -- Todos os crimes próximos de prescrever;
    -- Algum crime prescrito;
    -- Algum crime próximo de prescrever.

Alguns outros alertas estão disponíveis, porém não estão "ativados" no código, já que ainda precisam ser revistos e testados:

- Documentos criminais sem retorno do TJ há mais de 60 dias;
- Documentos não criminais sem retorno do TJ há mais de 120 dias;
- Documentos com Órgão Responsável possivelmente desatualizado.

Explicando rapidamente um a um, temos:

Documentos com novas ITs do GATE
    O alerta é levantado para documentos que possuem uma IT do GATE e que não tiveram vistas abertas depois da data da IT. Isso vale também para documentos que nunca tiveram vistas abertas. Aqui são considerados todos os documentos, sem filtros por classe, por status ou fase, o que quer dizer que até mesmo documentos que foram cancelados ou que constam no sistema como concluídos serão levados em consideração, caso não tenham tido vistas abertas depois de uma IT do GATE.

ICs sem prorrogação por mais de um ano
    São considerados documentos que não foram cancelados e que ainda estão como Em Andamento no sistema, e que sejam da classe de IC, conforme a tabela abaixo:
    
    +-----------------------------------+-----------------------------------+
    | cldc_dk                           | hierarquia                        |
    +===================================+===================================+
    | 392                               | EXTRAJUDICIAIS > PROCEDIMENTOS DO |
    |                                   | MP > Inquérito Civil              |
    +-----------------------------------+-----------------------------------+

    Esses documentos não podem ter correlacionamento do tipo "Apenso" ou "Anexo" com outros documentos. Além disso, o documento precisa ter tido pelo menos um andamento, que não tenha sido cancelado, dos seguintes tipos:

    +-----------------------------------+-----------------------------------+
    | tppr_dk                           | hierarquia                        |
    +===================================+===================================+
    | 6291                              | MEMBRO > Despacho > Prorrogação   |
    |                                   | de Prazo de Investigação          |
    +-----------------------------------+-----------------------------------+
    | 6511                              | MEMBRO > Conversão > Conversão de |
    |                                   | Procedimento Administrativo em    |
    |                                   | Inquérito Civil                   |
    +-----------------------------------+-----------------------------------+
    | 6012                              | MEMBRO > Portaria > Instauração   |
    |                                   | de Inquérito Civil                |
    +-----------------------------------+-----------------------------------+
    | 6002                              | MEMBRO > Conversão > Conversão de |
    |                                   | Procedimento Preparatório em      |
    |                                   | Inquérito Civil                   |
    +-----------------------------------+-----------------------------------+

    O alerta é ativado nos casos em que a data do andamento mais recente (dos tipos acima) ocorreu há mais de um ano.

Documentos com vitimas recorrentes recebidos nos ultimos 30 dias
    Para este alerta, são considerados os documentos (que tenham sido cancelados ou não, que estejam Em Andamento ou não) que tenham personagens com os seguintes tipos:
    
    +-----------------------------------+-----------------------------------+
    | tppe_dk                           | descricao                         |
    +===================================+===================================+
    | 3                                 | Vítima                            |
    +-----------------------------------+-----------------------------------+
    | 290                               | Autor do fato/vítima              |
    +-----------------------------------+-----------------------------------+

    Além disso, a coluna de matéria do documento (docu_mate_dk) deve estar associada à matéria do seguinte tipo (a descrição se encontra na tabela MPRJ_MATERIA_MGP schema MPRJ do Oracle - não está no BDA):

    +-----------------------------------+------------------------------------------------+
    | mate_dk                           | descricao                                      |
    +===================================+================================================+
    | 43                                | Violência Doméstica e Familiar contra a Mulher |
    +-----------------------------------+------------------------------------------------+

    Em seguida, com esses documentos em mãos, são selecionados aqueles cuja data de cadastro ocorreu dentro dos últimos 30 dias. Os personagens de cada um desses documentos recentes serão então comparados com os personagens de todos os outros documentos (tanto os mais antigos, quanto os outros que também ocorreram neste intervalo de 30 dias). Desta forma, caso uma vítima tenha aparecido em dois documentos recentes, o alerta será levantado para estes dois documentos.

    Dois personagens em documentos diferentes são considerados a mesma pessoa caso:

    - A chave primária de pessoa na tabela (pess_dk) for igual;
    - O CPF dos dois existem e são iguais (com exceção de CPFs = 00000000000);
    - O RG dos dois existem e são iguais;
    - O nome da pessoa, e o nome da mãe na tabela existem e são iguais;
    - O nome da pessoa, e a data de nascimento dela existem e são iguais.

    Caso essas comparações encontrem a mesma pessoa em outros documentos, o alerta é levantado para aquele documento.
    

Ofício fora do prazo
    Para este alerta, são considerados documentos que não foram cancelados, e que ainda estão Em Andamento no sistema. Eles também devem possuir obrigatoriamente um andamento do seguinte tipo:

    +-----------------------------------+------------------------------------------------+
    | tppr_dk                           | hierarquia                                     |
    +===================================+================================================+
    | 6497                              | SERVIDOR > Cumprimento de Diligências > Ofício |
    +-----------------------------------+------------------------------------------------+

    Caso o documento possua mais de um andamento deste tipo, para fins do alerta será considerado o mais antigo (ou seja, que gerou o alerta primeiro). O alerta é levantado caso a data de andamento do ofício mais antigo tenha ocorrido há mais de um ano.

    É importante notar que, caso o documento tenha tido um andamento de ofício, este alerta será gerado ad eternum, até que o documento seja cancelado ou concluído no sistema. Não há, atualmente, nenhuma verificação de cumprimento do ofício para parar de gerar o alerta.

    !! PARECE TER UM BUG AQUI, o andamento usado é "Cumprimento de Diligências", então parece que esse seria um andamento para parar de gerar o alerta, e não para começar a gerar. Buscando os tipos de Andamentos com "Ofício" no nome, acham-se os seguintes tipos:

    - 6614	MEMBRO > Despacho > Expedição de Documento > Ofício > Via Grupo de Apoio aos Promotores (GAP) 
    - 6615	MEMBRO > Despacho > Expedição de Documento > Ofício > Via Técnico de Notificações (TNAI) 
    - 6616	MEMBRO > Despacho > Expedição de Documento > Ofício > Outros meios
    - 6617	SERVIDOR > Cumprimento de Diligências > Ofício > Via Grupo de Apoio aos Promotores (GAP) 
    - 6618	SERVIDOR > Cumprimento de Diligências > Ofício > Via Técnico de Notificações (TNAI) 
    - 6619	SERVIDOR > Cumprimento de Diligências > Ofício > Outros meios
    - 6497	SERVIDOR > Cumprimento de Diligências > Ofício
    - 6581	MEMBRO > Despacho > Expedição de Documento > Ofício
    - 6126	SERVIDOR > Área Administrativa/CGMP > Diligências > Ofício
    - 1042	Autuação de Expediente administrativo como Inquérito civil "de ofício"
    - 6989	MEMBRO > ATOS COMUNS > Diligências > Ofício
    - 7436	SERVIDOR > ATOS COMUNS > Diligências > Ofício
    - 6211	SERVIDOR > Área Administrativa/CGMP > Regularização de pendências > Resposta de ofício

    !! Bater isso com o Matheus, porque a regra de negócio deste alerta não parece estar correta

Expedientes de Ouvidoria (EO) pendentes de recebimento
    asdasdasd

Procedimento Preparatório fora do prazo
    asdafasfasf

PAs sem prorrogação por mais de um ano
    saeqwrasf

Vistas abertas em documentos já fechados
    teweyeryery

Notícia de Fato a mais de 120 dias
    wrqesdgvs

Movimento em processo de segunda instância
    rwgsdgrt

Alertas de prescrição
    Este alerta possui várias etapas, de forma que elas serão descritas uma por uma.

    1 - Consideram-se os documentos que estão "Em Andamento" e que não foram cancelados, cuja data de cadastro no sistema seja maior do que 2010-01-01. Apenas são considerados os documentos associados a PIPs.
    Buscam-se então os assuntos destes documentos e, utilizando-se de uma tabela feita manualmente com as penas de cada delito, temos os documentos e seus crimes associados às suas penas máximas. Os assuntos que ainda não tem pena máxima preenchida são descartados, assim como aqueles que já atingiram sua data de fim no sistema.

    Outro ponto importante nesta etapa é que, para os cálculos subsequentes, caso a data do fato não exista, ou caso ela seja maior do que a data de cadastro do documento no sistema, então a data de cadastro do documento será utilizado como data do fato. Por isso, ao falarmos sobre "data do fato" nas próximas etapas, tenha em mente que ela pode ser tanto a data do fato tal qual registrada, ou a data de cadastro, vistas estas condições.

    2 - Com os documentos/crimes e suas penas em mãos, é necessário ver se, dentre estes crimes, há algum que funcione como multiplicador. Ou seja, um crime que apenas aumente/diminua a pena dos outros crimes do mesmo documento. Caso haja, será calculado um "fator da pena", que servirá para recalcular a pena máxima. Esse fator é multiplicativo, relativo a todos os crimes multiplicadores presentes no documento.

    Ex.1: Em um documento, há um crime de "Homicídio Qualificado", cuja pena máxima é de 30 anos. No mesmo documento, no entanto, também está associado o crime de "Crime Tentado", que funciona como um multiplicador com valor de 2/3. A pena máxima fatorada, para o crime de "Homicídio Qualificado" neste documento, será, portanto, de 20 anos.
    
    Ex.2: Em outro documento, há o mesmo crime, "Homicídio Qualificado". No entanto, neste documento, por algum motivo, o crime de "Crime Tentado" está associado 2 vezes. Neste caso, o cálculo será feito com um fator de valor 2/3 * 2/3 = 4/9. Ou seja, a pena máxima, que inicialmente é de 30 anos, irá para 13,33 anos.

    3 - Com a pena máxima fatorada, é possível, então, calcular o tempo de prescrição do documento, seguindo a seguinte regra:

        - max_pena_fatorado < 1, tempo de prescrição = 3
        - max_pena_fatorado < 2, tempo de prescrição = 4
        - max_pena_fatorado < 4, tempo de prescrição = 8
        - max_pena_fatorado < 8, tempo de prescrição = 12
        - max_pena_fatorado < 12, tempo de prescrição = 16
        - Senão, tempo de prescrição = 20

    4 - Com o tempo de prescrição em mãos, será calculado um fator do tempo de prescrição, a partir dos personagens investigados do documento. Basicamente, para cada investigado do documento, serão calculadas as datas de aniversário de 21 anos e de 70 anos. Com essas datas, verificamos:
        
    - Se a idade do investigado é igual ou maior do que 70 anos;
    - Se a idade do investigado era menor do que 21 anos na data do fato (ou data de cadastro como explicado anteriormente).
    
    Caso uma destas condições seja verdadeira, o tempo de prescrição de cada um dos crimes, para aquele investigado, é cortado pela metade. O tempo de prescrição para os demais investigados não é afetado, a não ser que os outros investigados também cumpram essas condições.

    Os tipos de personagem no sistema considerados para esta etapa são os seguintes:

    +----------------+-----------------------------+
    | tppe_dk        | descrição                   |
    +----------------+-----------------------------+
    | 5.0000000000   | Réu                         |
    +----------------+-----------------------------+
    | 7.0000000000   | Autor(a)                    |
    +----------------+-----------------------------+
    | 14.0000000000  | Investigado(a)              |
    +----------------+-----------------------------+
    | 20.0000000000  | Denunciado(a)               |
    +----------------+-----------------------------+
    | 21.0000000000  | Autor(a) do Fato            |
    +----------------+-----------------------------+
    | 24.0000000000  | ACUSADO                     |
    +----------------+-----------------------------+
    | 32.0000000000  | Reclamado                   |
    +----------------+-----------------------------+
    | 40.0000000000  | Representado(a)             |
    +----------------+-----------------------------+
    | 290.0000000000 | Autor do fato/vítima        |
    +----------------+-----------------------------+
    | 317.0000000000 | Autuado                     |
    +----------------+-----------------------------+
    | 345.0000000000 | Representado (Corregedoria) |
    +----------------+-----------------------------+

    Pessoas físicas com nome "MP" também são descartados, caso apareçam como investigadas no documento.

    5 - Calculado o tempo de prescrição fatorado para cada crime e cada personagem, a próxima etapa será calcular a data inicial da prescrição. Ela será escolhida com a seguinte ordem de prioridade:

    - Se um crime for classificado como abuso de menor, e a vítima tiver menos de 18 anos na data do fato, então a prescrição começará a contar a partir da data de aniversário de 18 anos da vítima. Caso haja mais de uma vítima menor de idade na data do fato, será utilizada a data de aniversário da mais nova (ou seja, a maior data de aniversário de 18 anos);
    - Se tiver ocorrido um andamento de Rescisão de Acordo de Não Persecução Penal (andamento de tppr_dk = 7920), a data inicial da prescrição será a data do andamento de rescisão;
    - Senão, utiliza-se a data do fato (ou data cadastro, nas condições em que não houver data do fato, ou se ela for maior do que a data de cadastro).

    Os seguintes tipos de personagem são considerados vítimas em um documento:

    +----------------+------------------------------------------+
    | tppe_dk        | descrição                                |
    +----------------+------------------------------------------+
    | 3.0000000000   | Vítima                                   |
    +----------------+------------------------------------------+
    | 6.0000000000   | ADOLESCENTE CARENTE                      |
    +----------------+------------------------------------------+
    | 13.0000000000  | Menor                                    |
    +----------------+------------------------------------------+
    | 18.0000000000  | ADOLESCENTE                              |
    +----------------+------------------------------------------+
    | 248.0000000000 | Adolescente/criança em situação de risco |
    +----------------+------------------------------------------+
    | 290.0000000000 | Autor do fato/vítima                     |
    +----------------+------------------------------------------+

    6 - Ao chegar nesta etapa, teremos informações sobre as datas inicias de prescrição, assim como o tempo de prescrição, para cada investigado e crime, em cada documento. Aqui, iremos apenas somar a data inicial de prescrição, com o tempo de prescrição, para obter a data final da prescrição. Também será calculada a diferença entre a data de hoje, e a data final da prescrição, obtendo o número de dias desde (ou para) a prescrição (ou seja, podendo ser positivo ou negativo no sistema).

    7 - A etapa final, consiste em utilizar esses valores calculados, do número de dias desde/para a prescrição do crime para aquele investigado, para identificar em qual subtipo de alerta o documento se encaixa. Isso é feito da seguinte maneira:

    - Caso o número de dias seja maior do que 0, dá-se o status "2" ao crime (indicando que já passou da prescrição);
    - Caso o número de dias esteja entre 0 e 90 (inclusive), dá-se o status "1" ao crime (indicando que está próximo de prescrever);
    - Senão, dá-se o status "0" ao crime (não prescreveu, nem está próximo).

    Então, com o status de cada crime em mãos, é feita uma análise para ativar um de 4 alertas possíveis:
    - PRCR1 - Caso todos os crimes do documento estejam prescritos para todos os investigados;
    - PRCR2 - Caso todos os crimes do documento estejam próximos de prescrever para todos os investigados;
    - PRCR3 - Caso algum crime (mas não todos) do documento esteja prescrito;
    - PRCR4 - Caso algum crime (mas não todos) do documento esteja próximo de prescrever.

    Um documento que acenda um alerta de prescrição só pode estar presente em um destes subtipos de alerta.

    De forma mais detalhada, a análise dos status dos crimes é feita da seguinte maneira:

    - Se o ``min(status)`` do documento for "2", quer dizer que todos os crimes estão prescritos para todos os investigados, e ele é então colocado no alerta PRCR1 (todos os crimes prescritos);
    - Se o ``min(status)`` do documento for "1", quer dizer que todos os crimes estão próximos de prescrever, para todos os investigados. Pode haver alguns crimes com status "2", mas se ``min(status)`` naquele documento é "1", então todos os restantes estão próximos, e ele é então colocado no alerta PRCR2 (todos os crimes próximos de prescrever).
    - Se o ``max(status)`` do documento for "2", quer dizer que algum crime está prescrito (mas não todos). É importante notar que essas condições são avaliadas em ordem. Então, para chegar nesta condição, as duas primeiras precisam necessariamente ser falsas. Ou seja, o ``min(status)`` do documento tem de ser "0". Isso indica que um ou mais crimes prescreveram, e um ou mais crimes não estão próximos de prescrever. Alguns podem ter status "1", estando próximos, mas como não são todos, o documento deve ser colocado no alerta PRCR3 (algum crime prescrito).
    - Finalmente, se o ``max(status)`` do documento for "1", quer dizer que não há crimes prescritos, mas alguns estão próximos de prescrever, enquanto outros não estão próximos. Isso faz com que este documento seja colocado no alerta PRCR4 (algum crime próximo de prescrever).

    E com isso, temos, para cada documento, o tipo de alerta em que ele se encontra.

    Exemplo para ilustração:

    Há um procedimento com um único investigado, e 3 crimes:
	- Ameaça;
	- Estupro de Vulnerável (abuso_menor = 1);
	- Atentado Violento ao Pudor (abuso_menor = 1).

	Ou seja, 2 crimes classificados como abuso de menor, e 1 que não é abuso de menor.

	Nesse exemplo, a data do fato é 2016-06-01. Mas a vítima, de acordo com o sistema, era menor de idade, e a data de 18 anos dela é 2020-07-17.
	Então, a data inicial de prescrição será feita dessa forma:

	- Ameaça: Data Inicial de Prescrição em 2016-06-01;
	- Estupro de Vulnerável: Data Inicial de Prescrição em 2020-07-17;
	- Atentado Violento ao Pudor: Data Inicial de Prescrição em 2020-07-17.

	E então, dessa forma, haverá um crime com data final de prescrição em 2019-06-01 (o de Ameaça, 3 anos a partir da data inicial dele em 2016-06-01) e os outros dois com data final de prescrição em 2036-07-17 (Atentado ao Pudor, 16 anos a partir do aniversário de 18 da vítima), e 2040-07-17 (Estupro de Vulnerável, 20 anos a partir do aniversário de 18 da vítima). Se estivermos olhando para este documento no dia 2020-10-01, nesta data há um crime prescrito (o de Ameaça) e dois crimes ainda não-prescritos. Por conta disso, ele é colocado no alerta PRCR3, porque algum crime está prescrito, mas não todos.


Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: MMPS_ALERTAS
   Colunas: 
      alrt_docu_dk (int)
      alrt_docu_nr_mp (string)
      alrt_docu_nr_externo (string)
      alrt_docu_etiqueta (string)
      alrt_docu_classe (string)
      alrt_docu_date (timestamp)
      alrt_orgi_orga_dk (int)
      alrt_classe_hierarquia (string)
      alrt_dias_passados (int)
      alrt_descricao (string)
      alrt_sigla (string)
      alrt_session (string)
      dt_partition (string)
    
A geração da tabela no BDA é feita da seguinte maneira:

Cada alerta é separado em um script separado, com uma função que realiza os cálculos necessários para aquele alerta específico. Os cálculos e metadados dos cálculos em si não são salvos na tabela final de alertas, eles são apenas utilizados para dizer quais documentos ativaram aquele alerta.

No script principal (Jobs_), os alertas são associados a siglas, descrições e suas funções respectivas. Cada uma dessas funções é então chamada, e o resultado é utilizado para salvar os resultados numa tabela temporária (com uma coluna indicando a qual tipo de alerta aqueles resultados pertencem - ``alrt_sigla``). Ao fim deste processo, a tabela temporária é então utilizada para escrever na tabela final ``MMPS_ALERTAS``. Além disso, informações daquela sessão de cálculo são salvas na tabela ``MMPS_ALERTA_SESSAO``. Esta tabela será usada no backend para definir a sessão mais recente, e pegar os alertas correspondente a ela.

A coluna ``dt_partition`` é utilizada para particionar a tabela de acordo com a data do cálculo. Também vale dizer que as tabelas ``MCPR_DOCUMENTO`` e ``MCPR_VISTA`` são cacheadas no início deste processo, para melhorar o desempenho dos cálculos que as utilizam frequentemente.

Em seguida, vamos explicitar melhor o processo e regras utilizadas em cada um dos alertas implementados:

GATE
^^^^
Documentos com novas ITs do GATE

AlertaGate_

O que este alerta faz é basicamente:
- Pega a vista mais recente, max(dt_abertura_vista), para cada documento;
- Pega as datas de IT do GATE para cada documento;
- Filtra as ITs para considerar apenas aquelas que ocorreram depois da max(dt_abertura_vista);
- Se tiver mais de uma IT no documento nessa condição, considera-se a mais antiga, que ativou o alerta primeiro.

Também são consideradas as ITs de documentos que não tiveram vista aberta ainda. Assim, se tiver ITs mais recentes do que a última vista (ou doc sem vista), o alerta será ativado para aquele documento.


IC1A
^^^^

MVVD
^^^^

OFFP
^^^^

OUVI
^^^^

PA1A
^^^^

PPFP
^^^^

VADF
^^^^

NF30
^^^^

DT2I
^^^^

PRCR
^^^^

- se data do fato não existir ou for maior que data de cadastro usa data de cadastro
- se pena for nula desconsidera
- se o documento não estiver Em Andamento, ou tiver sido cancelado, descarta
- consideram-se apenas documentos com data de cadastro depois de 2010-01-01
- apenas pacotes de PIPs
- se o asdo_dt_fim estiver definido para um assunto, desconsidera (assunto cancelado)
- se alguma pena no documento for de assunto multiplicador multiplica tudo pelo fator
- se o cara tiver menos de 21 ou >= 70 na data do fato ou data atual divide tempo de prescrição por 2 (usando os mesmos tipos de personagens que definimos pros investigados da PIP)
- data inicial de prescrição com a hierarquia de: 
    - se for abuso de menor e o menor tiver menos de 18 anos na data do fato (ou data de cadastro nas condições do primeiro ponto), usa a data de 18 anos como data inicial
    - se tiver acordo de não persecução penal e tiver rescisão, usa a data do andamento de rescisão do ANPP
    - senão, usa data do fato (ou data de cadastro nas condições lá)
- data final de prescrição = data inicial + tempo de prescrição
- Alerta é dividido em 4 subtipos: PRCR1 (todos os crimes prescritos - para todos os investigados), PRCR2 (todos os crimes próximos de prescrever - para todos os investigados), PRCR3 (algum crime prescrito), PRCR4 (algum crime próximo de prescrever).

Também é gerada uma tabela de detalhes do alerta PRCR, com os metadados do cálculo.


.. _Jobs: https://github.com/MinisterioPublicoRJ/alertas/blob/develop/src/alertas/jobs.py
.. _AlertaGATE: https://github.com/MinisterioPublicoRJ/alertas/blob/optimization/alertas/src/alertas/alerta_gate.py

View Backend
************

::

   GET dominio/endpoint/

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
       "atributo1": 1,
       "atributo2": 2,
   }

Nome da View: `ViewTal`_.

.. _ViewTal: url da view no github

Dependências
~~~~~~~~~~~~

- Dependência 1
- Dependência 2

Troubleshooting
~~~~~~~~~~~~~~~
