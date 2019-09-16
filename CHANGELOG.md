## [Unreleased]
### Added
 - Inclusão da API do MPRJ Digital no sistema
 - Controle de alterações por meio de CHANGELOG
 - Configurações diferenciadas para teste
## [1.1.1] - 2019-09-16
### Added
 - Inclusão de testes automatizados com Travis CI
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
<<<<<<< HEAD
=======
>>>>>>> Adição de Changelog
=======
>>>>>>> Migrações e configurações de teste para o MPRJ+
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