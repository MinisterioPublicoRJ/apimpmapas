==========
Introdução
==========

A intenção destes arquivos é documentar aspectos relevantes do Promotron, tais como os componentes existentes, como é feito o cálculo de cada componente, as regras de negócio utilizadas, possíveis passos para realizar o troubleshooting dos componentes, etc.

!! Frases precedidas por "!!" indicam possíveis problemas ou dúvidas encontrados durante a escrita desta documentação, em relação ao conteúdo.

++ Frases precedidas por "++" indicam possíveis melhoras/mudanças na própria documentação. Ou seja, em relação à forma.


Alguns dos objetivos para esta documentação são:

- Oferecer um Know-How das tabelas do MGP: Todos os cálculos advêm das tabelas do MGP, então entender estas tabelas é fundamental (e manter queries que permitam entender).
- Para cada componente, entender:
   - O funcionamento básico dele (Quase como um user manual para o promotor - responde O quê estou vendo)
   - Regras de negócio (se as regras estiverem em uma tabela/componente específico, referenciar - mas não repetir - as regras)
   - Estrutura do código (foco no back/BDA), vantagens/desvantagens? Outros aspectos? Cache, é real-time (oracle) ou impala?
   - Do que eles dependem (quais tabelas auxiliares/outros componentes que eles usam)
- Evitar repetir documentação. A documentação de um componente/tabela deve ser auto-contida para evitar duplicação em várias partes (o que dificulta manter o código). Isso quer dizer que, se o componente A depende de B, e tiver uma modificação em B, toda essa modificação será documentada em B (não em A), a não ser que a dependência mude, mas isso pressupõe que A também mudou.
- Troubleshooting (se possível, oferecer passos para resolução de possíveis problemas com o componente, levando em conta back e BDA)


Aspectos Iniciais
-----------------

Por enquanto, o Promotron só está implementado para as promotorias de Tutela Coletiva (com exceção das Tutelas Coletivas de infância ou de idoso), e para as PIPs Territoriais, Promotorias de Investigação Penal Territoriais (ou seja, as Especializadas não estão sendo consideradas). Ao falar "PIP" nesta documentação, refere-se às PIPs Territoriais.

!! Atualmente, para definir se uma promotoria é válida e algo deve ser mostrado para ele, busca-se o tipo da promotoria no backend (função tipo_orgao no apimpmapas/login/jwtlogin.py). Esta função remove as Tutelas de Idoso e/ou Infância. Porém não remove as PIPs Especializadas (que virão com muitos dados faltantes - já que não há atribuição definida para estas no BDA).

.. _introducao-atribuicao:

Atribuição
----------

O conceito de **atribuição** (ou **pacote de atribuição**) é muito usado no projeto como um todo, por isso vale a pena explicá-lo. Para fins dos cálculos realizados, a atribuição nada mais é do que um grupo de promotorias similares - e que portanto faz sentido de serem comparadas de forma conjunta. Um exemplo disso são as Promotorias de Tutela Coletiva de Cidadania.

- Tutelas Coletivas: a atribuição diz respeito ao pacote de atribuição no qual a Tutela está inserida (Consumidor, Cidadania, etc).
- PIPs: a atribuição diz respeito a todas as PIPs Territoriais.

As atribuições estão definidas na tabela auxiliar do BDA de nome ``atualizacao_pj_pacote``, e podem ser modificadas ou adicionadas (por exemplo, a atribuição de código 200 foi criada especificamente para as PIPs).


Ciclo de geração
----------------

++(Fazer um fluxograma disso?)

Tabelas podem ser criados por processo spark + NiFi, ou SQL rodado uma vez (tabelas auxiliares)

Script criação BDA -> Tabela -> View Backend -> Front
Ou Oracle -> View Backend -> Front

(Explicação sobre ambiente de produção e dev aqui?)

(Explicação sobre o que é um componente/subcomponente no escopo deste documento?)
Exemplo de Componente - Resumo do Dia, subcomponentes Frase de Acervo, Frase de Entradas, Frase de Resolutividade

O subcomponente é sempre relativo a uma view, enquanto o componente pode ser um conjunto de views.


Seções
------

- Know-How MGP
- Tabelas Auxiliares
- Componentes:
   - Para cada subcomponente:
   - User Manual
   - Regras de Negócio
   - Estrutura do Código
   - Dependências (pra trás - nunca pra frente) + Referências
   - Troubleshooting
