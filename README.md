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

```bash
pip install -r dev-requirements.txt
```

O projeto precisa do GDAL instalado no ambiente
No Debian/Ubuntu use:

```bash
sudo apt-get install binutils libproj-dev gdal-bin
```

# Rodando os testes

```bash
make test
```
