Principais Investigados
=======================

.. contents:: :local:

Construção dos Grupos de Investigados
-------------------------------------

Antes de analisar os investigados de cada promotoria e poder mostrar isso ao promotor, é necessário fazer um agrupamento dos investigados que são similares no sistema. Essa etapa é essencial pois, uma mesma pessoa (na vida real) pode estar associada a mais de uma pessoa no sistema. Isso faz com que a tarefa de mostrar todos os documentos associados a uma determinada pessoa (na vida real) se torne difícil.

Para construir este agrupamento, é feita o seguinte cálculo:

Primeiramente, é feita uma busca no sistema por todas as pessoas (ou seja, todos os ``pess_dk``) ligadas a personagens que já apareceram como investigados. Os personagens dos seguintes tipos são considerados investigados:

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

Em seguida, são recolhidas as seguintes informações destas pessoas:

Caso seja uma pessoa física:
- Nome;
- Nome da mãe;
- Data de nascimento;
- CPF;
- RG.

Caso seja uma pessoa jurídica:
- Nome;
- CNPJ.

Algumas limpezas também são realizadas nesta etapa, como por exemplo, retirar todos os caracteres que não são numéricos dos campos de CPF, RG e CNPJ. Também são retirados os caracteres com acentos dos nomes, e todos são colocados em maiúsculo - o que facilitará comparações mais à frente. Também são retiradas aquelas pessoas (físicas ou jurídicas) cujo nome remetam ao Ministério Público.

Com estes dados em mãos, são feitas diversas comparações entre os campos para agrupar estas pessoas. Duas pessoas físicas são consideradas a mesma pessoa (na vida real) nos seguintes casos:

- Se têm o mesmo ``pess_dk``;
- Se possuem o mesmo CPF (excetuando-se os casos em que o CPF é nulo, ou em que ele exista mas tenha valor igual a '00000000000');
- Se possuem a mesma data de nascimento (não pode ser nula) e mesmo RG (excetuando-se os casos em que o RG tenha valor igual a '000000000', ou não tenha exatamente 9 dígitos); !!(Bug a resolver: precisa verificar que RG também não é nulo)
- Se possuem a mesma data de nascimento e nomes similares (data de nascimento não-nula).
- Se possuem o nome similar, e o nome da mãe similar (o nome da mãe não pode ser nulo ou vazio, e também não pode conter "IGNORADO", "IDENTIFICADO" ou "DECLARADO" no nome - que seria um indicativo de um nome da mãe que não foi explicitado).
- Se possuem o nome similar e o mesmo RG (excetuando-se os casos em que o RG tenha valor igual a '000000000', ou não tenha exatamente 9 dígitos);

++ Explicar um pouco de como é feita a similaridade de nomes no difflib.SequenceMatcher do python ou foge do escopo?

Para o caso de pessoas jurídicas, esta comparação é análoga, porém mais simples:

- Se têm o mesmo ``pess_dk``;
- Se possuem o mesmo CNPJ (excetuando-se os casos em que o CNPJ é '00000000000000' ou '00000000000'.

Para formação do grupo final, é necessário associar cada ``pess_dk`` do sistema a um número identificador do grupo a que ele pertence. O número utilizado para representar o grupo é simplesmente o menor ``pess_dk`` presente no grupo.

Isto tudo feito, já temos a formação de um primeiro grupo de pessoas do sistema, associadas a um número que representa o grupo, chamado de "representante". Uma última etapa é feita para limpar possíveis "pulos" na formação dos grupos. É possível, por exemplo, que aconteça o seguinte cenário:

- A pessoa 1 é representante de si mesma (mesmo pess_dk);
- A pessoa 1 também é representante da pessoa 2 (ligadas por CPF);
- A pessoa 2 é representante da pessoa 3 (ligadas por data de nascimento e RG).

No entanto, neste cenário, há a formação de dois grupos (um grupo com as pessoas 1 e 2, e outro com a pessoas 3). Como não é possível ligar a pessoa 1 à pessoa 3 diretamente, forma-se um "pulo" nos grupos. Para resolver este problema, uma etapa adicional é realizada em que, caso uma pessoa 3 seja representada por uma pessoa 2, e esta pessoa 2 esteja representada por uma pessoa 1, então faz-se a ligação diretamente entre a pessoa 3 e 1.

++ Esta última etapa só está configurada para pulos de tamanho 1. É necessário verificar e modificar esta etapa para pulos de tamanhos maiores.


URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/develop/robo_promotoria/src/tabela_pip_investigados_representantes.py


Contagem dos Principais Investigados
------------------------------------

User Manual
~~~~~~~~~~~

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: TB_EXEMPLO
   Colunas: 
      coluna1 (int)
      coluna2 (int)
    

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/develop/robo_promotoria/src/tabela_pip_investigados.py

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


Perfil do Investigado
---------------------

User Manual
~~~~~~~~~~~

Estrutura do Código
~~~~~~~~~~~~~~~~~~~

Processo BDA
************

::

   Nome da Tabela: TB_EXEMPLO
   Colunas: 
      coluna1 (int)
      coluna2 (int)
    

URL do Script: https://github.com/MinisterioPublicoRJ/scripts-bda/blob/master/robo_promotoria/src/tabela_dist_entradas.py.

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