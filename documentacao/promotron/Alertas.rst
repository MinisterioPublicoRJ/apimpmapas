Alertas
=======

.. contents:: :local:

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

Alguns outros alertas estão disponíveis, porém não estão "ativados" no código:

- Documentos criminais sem retorno do TJ a mais de 60 dias;
- Documentos não criminais sem retorno do TJ a mais de 120 dias;
- Documentos com Órgão Responsável possivelmente desatualizado.

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

Cada alerta é separado em um script separado, com uma função que faça os cálculos necessários para aquele alerta específico, retornando o resultado deste cálculo. No script principal (Jobs_), os alertas são associados a siglas, descrições e suas funções respectivas. Cada uma dessas funções é então chamada, e o resultado é utilizado para salvar os resultados numa tabela temporária (com uma coluna indicando a qual tipo de alerta aqueles resultados pertencem - ``alrt_sigla``). Ao fim deste processo, a tabela temporária é então utilizada para escrever na tabela final ``MMPS_ALERTAS``.

A coluna ``dt_partition`` é utilizada para particionar a tabela de acordo com a data do cálculo. Também vale dizer que as tabelas ``MCPR_DOCUMENTO`` e ``MCPR_VISTA`` são cacheadas no início deste processo, para melhorar o desempenho dos cálculos que as utilizam frequentemente.

Em seguida, vamos explicitar melhor o processo e regras utilizadas em cada um dos alertas implementados:

GATE
^^^^
Documentos com novas ITs do GATE

AlertaGate_

!! Parece ter um bug. São pegos os ITs que tem vista mais recente do que ele, e o min(dt_it), ao invés de max. Também não é filtrada a max(vist_dt_abertura_vista), sendo consideradas todas.


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


.. _Jobs: https://github.com/MinisterioPublicoRJ/alertas/blob/develop/alertas/src/alertas/jobs.py
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
