[![Build Status](https://travis-ci.com/MinisterioPublicoRJ/apimpmapas.svg?branch=develop)](https://travis-ci.com/MinisterioPublicoRJ/apimpmapas)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/83cecc0446464afc91bfa1efb5e46878)](https://www.codacy.com/manual/SamambaMan/apimpmapas?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MinisterioPublicoRJ/apimpmapas&amp;utm_campaign=Badge_Grade)

# Configurar o projeto

Para rodar este projeto localmente você deve criar um ambiente virtual (i.e: [virtualenv](https://virtualenv.pypa.io/en/latest/)).
Em seguida, você deve acionar seu virtualenv. A forma de ativar o ambiente depende da forma que este
foi criado:

```bash
python -m venv <nome-do-env>

source <nome-do-env>/bin/activate
```

```bash
mkvirtualenv <nome-do-env>

workon <nome-do-env>
```

```bash
pyenv virtualenv 3.7.2 <nome-do-env>

pyenv actiave <nome-do-env>
```

e em seguida clone o repositório:

```bash
git clone https://github.com/MinisterioPublicoRJ/apimpmapas.git
```

## Instalar dependências

Caso algum dado a ser usado seja originado de alguma base Oracle,
será necessário instalar o Oracle instant client
No Debian/Ubuntu siga as instruções:
https://help.ubuntu.com/community/Oracle%20Instant%20Client

O projeto precisa do GDAL instalado no ambiente
No Debian/Ubuntu use:

```bash
sudo apt-get install binutils libproj-dev gdal-bin
```

Em seguida devem ser instaladas as dependências Python

```bash
pip install -r dev-requirements.txt
```

# Rodando os testes

```bash
make test
```

# Rodando os testes de integração
Esse teste valida o acesso real aos bancos usados - PostgreSQL, Oracle e Impala.
Assim, as configurações de acesso devem estar corretamente registradas em um arquivo
de configurações ou variáveis de ambiente.

Para rodar os testes é necessário antes do comando "make test" exportar a 
variável de ambiente INTEGRATION_TEST.
No Debian/Ubuntu faça

```bash
export INTEGRATION_TEST=1
```
