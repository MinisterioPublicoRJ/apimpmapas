## [Unreleased]
## [1.1.9]
### Changed
 - Adição de sistema de cache para as visualizações
## [1.1.8]
### Changed
 - Alteracão para permitir discrição entre link de imagem e campo base64 para lista de pessoas
## [1.1.7]
### Changed
 - Data Check Feature - command para verificação básica de integridade de Caixinhas por Entidade
 - Move To Position - Possibilidade de mover uma caixinha para uma posição específica na ordem de caixinhas através de django admin actions
## [1.1.6]
### Changed
 - BUGFIX - Correção na validação de OSM: Entidades causam erro de entidade OSM já vinculada ao serem editadas (de novo)
## [1.1.5]
### Added
 - Adição de seletor de exibição nas caixinhas
## [1.1.4] - 2019-09-25
### Changed
 - BUGFIX - Correção na validação de OSM: Entidades causam erro de entidade OSM já vinculada ao serem editadas
## [1.1.3] - 2019-09-20
### Changed
 - Extração de ícones de apps diferentes para uma app unificada
## [1.1.2] - 2019-09-17
### Added
 - Inclusão da API do MPRJ Digital no sistema
 - Controle de alterações por meio de CHANGELOG
 - Configurações diferenciadas para teste
## [1.1.1] - 2019-09-16
### Added
 - Inclusão de testes automatizados com Travis CI
### Changed
 - BUGFIX - Correção na lógica de busca espacial
## [1.1.0] - 2019-09-09
### Added
 - Permissões de acesso - Entidades e dados podem ser configurados com grupos específicos de acesso, sendo bloqueado o acesso por usuários não pertencentes a estes grupos.
## [1.0.5] - 2019-09-09
### Changed
 - BUGFIX - Cor padrão de temas alterada de branco para preto
## [1.0.4] - 2019-09-06
### Changed
 - BUGFIX - Correção nas opções de colunas
## [1.0.3] - 2019-09-06
### Added
 - BUGFIX - Correção no acesso às bases PostgreSQL
 - Inclusão de opção de coluna "Sufixo de título"
### Changed
 - Tradução dos títulos no painel administrativo
 - Campo ExhibitionField exibido no painel administrativo
## [1.0.2] - 2019-09-03
### Added
 - BUGFIX - Configurações de CORS
### Removed
 - Removido pacote não binário do psycopg2 - acesso concentrado no binário
## [1.0.1] - 2019-08-29
### Added
 - BUGFIX - Permitido tema em branco no painel administrativo
 - BUGFIX - Tradução de tipos de colunas para evitar conflito com palavras reservadas de sistema
## [1.0.0] - 2019-08-27
### Added
 - Agrupamento de caixinhas por temas
 - Gráficos - Dados que representarem menos de 3% do total são agrupados numa única categoria "Outros"
### Changed
 - Conjunto fixo de colunas podendo incluir dados nulos substituído por lista variável de colunas
## [0.0.9] - 2019-08-07
### Added
 - Exibição de entidades
 - Listagem de caixinhas por entidade
 - Exibição de mapas em entidades com representação espacial
 - Painel de administração
