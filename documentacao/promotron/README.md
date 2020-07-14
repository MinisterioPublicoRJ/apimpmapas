# Documentação Promotron

A intenção destes arquivos é documentar aspectos relevantes do Promotron, tais como os componentes existentes, como é feito o cálculo de cada componente, as regras de negócio utilizadas, possíveis passos para realizar o troubleshooting dos componentes, etc.

Frases verdes precedidas por "!!" indicam possíveis problemas ou dúvidas encontrados durante a escrita deste notebook.

<font color="green">!! Aqui um exemplo de frase deste tipo, para facilitar identificar possíveis issues.</font>

## Aspectos Iniciais

Por enquanto, o Promotron só está implementado para as promotorias de Tutela Coletiva (com exceção das Tutelas Coletivas de infância ou de idoso), e para as PIPs Territoriais, Promotorias de Investigação Penal Territoriais (ou seja, as Especializadas não estão sendo consideradas). Ao falar "PIP" nesta documentação, refere-se às PIPs Territoriais.

<font color="green">!! Atualmente, para definir se uma promotoria é válida e algo deve ser mostrado para ele, busca-se o tipo da promotoria no backend (função tipo_orgao no apimpmapas/login/jwtlogin.py). Esta função remove as Tutelas de Idoso e/ou Infância. Porém não remove as PIPs Especializadas (que virão com muitos dados faltantes - já que não há atribuição definida para estas no BDA).</font>

#### Atribuição

O conceito de **atribuição** (ou **pacote de atribuição**) é muito usado no projeto como um todo, por isso vale a pena explicá-lo. Para fins dos cálculos realizados, a atribuição nada mais é do que um grupo de promotorias similares - e que portanto faz sentido de serem comparados de forma conjunta. Um exemplo disso são as Promotorias de Tutela Coletiva de Cidadania.

As atribuições estão definidas na tabela do BDA de nome exadata_aux(_dev).atualizacao_pj_pacote, e podem ser modificadas ou adicionadas (por exemplo, a atribuição de código 200 foi criada especificamente para as PIPs).
