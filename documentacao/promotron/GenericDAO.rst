.. _GenericDAO:

GenericDAO
----------

Classe utilizada para pegar uma query (definida em um arquivo .sql), executá-la no Impala, e retornar o resultado serializado (por meio, opcionalmente, de um Serializer).

++ Melhorar essa explicação, mas por enquanto deixar aqui para ser referenciado em outras partes da documentação.

.. _SingleDataObjectDAO:

SingleDataObjectDAO
-------------------

Herda a mesma funcionalidade do GenericDAO. No entanto, ao invés de retornar uma lista de objetos serializados, retorna apenas um (o primeiro da lista).

Útil para casos em que a resposta esperada da query do Impala possui uma única linha.